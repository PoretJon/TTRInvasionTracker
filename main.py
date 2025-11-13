"""
* Flippy! main.py
* Author: Jon Poret 2025
* Purpose: Runs the discord bot, providing functionality.
"""

import os, discord, dotenv
from typing import Literal
from discord.ext import commands, tasks
from Information import CogInformation
from Tracker.invasion import Invasion
from Tracker.invasion_obtainer import InvasionTracker
from Database.db_handler import FlippyDB
import time


cog_info = CogInformation.CogInformation()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
dotenv.load_dotenv(dotenv_path="Database/.env")
db_params = f"dbname={os.getenv("dbname")} user={os.getenv("user")} password={os.getenv("password")} host={os.getenv("host")} port={os.getenv("port")}"
flipDB = FlippyDB(db_params)
# tree = discord.app_commands.CommandTree(bot)


# creates a string of user ids, not very efficient
def build_ping_list(users: list):
    list = ""
    for user in users:
        list += f"@&{user} "
    return list


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)
    if not invasion_check_loop.is_running():
        invasion_check_loop.start()


@bot.tree.command(name="get_invasions", description="Get current invasions")
async def get_invasions(interaction):
    text = tracker.get_cur_invasions_message()
    await interaction.response.send_message(text)


async def cogname_autocomplete(
    interaction: discord.Interaction, current: str
) -> list[discord.app_commands.Choice[str]]:
    cogs = cog_info.cogs_dict.keys()
    choices = [
        discord.app_commands.Choice(name=cog, value=cog)
        for cog in cogs
        if current.lower() in cog.lower()
    ]
    return choices[:25]


@bot.tree.command(
    name="subscribe_to_cog",
    description="Subscribe to notifications for a specific cog.",
)
@discord.app_commands.autocomplete(cog=cogname_autocomplete)
async def subscribe_to_cog(interaction: discord.Interaction, cog: str):
    if cog not in cog_info.cogs_dict.keys():
        await interaction.response.send_message(
            "You have entered an incorrect cog name. Please try again.", ephemeral=True
        )
        return
    user_id = interaction.user.id
    print(user_id)
    res = flipDB.register_cog_for_user(user_id, cog)
    print(res)
    if res is not None:
        await interaction.response.send_message(f"{cog} registered")


@bot.tree.command(
    name="unsubscribe_to_cog", description="Unsubscribe from notifications for a cog."
)
@discord.app_commands.autocomplete(cog=cogname_autocomplete)
async def unsubscribe_from_cog(interaction: discord.Interaction, cog: str):
    # logic for unsubscribing
    user_id = interaction.user.id
    res = flipDB.remove_cog_ping(user_id, cog)
    if res is not None:  # assumes this always returns the correct thing, may not
        await interaction.response.send_message(f"Unsubscribed from {cog}")


@bot.tree.command(
    name="register_server",
    description="Registers the bot to this channel. Requires admin priveliges.",
)
@commands.has_permissions(administrator=True)
async def register_server(channel: discord.Interaction):
    channel_name = channel.channel_id
    guild_id = channel.guild_id
    flipDB.register_server(guild_id, channel_name)
    await channel.response.send_message(
        "Registered Flippy to this channel. If Flippy was registered in this server already, this channel will now be used instead."
    )


@bot.event
async def on_message(message):
    if message.author == bot.user:  # make sure the bot doesnt reply to itself
        return

    for cog_name in cog_info.cogs_dict:
        if cog_name.lower() in message.content.lower():
            msg = f"**Name:** {cog_name}\n**Type:** {cog_info.cogs_dict[cog_name]}"
            await message.channel.send(msg)
            return


# invasion check loop
# sends messages to my private server when new invasions are found
@tasks.loop(minutes=5)
async def invasion_check_loop():
    invasions = tracker.refresh_current_invasions()
    # check for new invasions
    new_invasions = invasions[0]
    ended_invasions = invasions[1]

    if len(new_invasions) > 0 or len(ended_invasions) > 0:
        # get all channels, create user list per server
        server_list = flipDB.get_server_list()
        for server in server_list:
            guild_id = server[0]  # TODO: double check this is correct
            for invasion in new_invasions:
                cog_name = invasion._cogType()
                ping_list = flipDB.get_all_pings_for_server(guild_id, cog_name)

    if len(invasions[0]) > 0:
        channel = bot.get_channel(1410048723743932547)
        for inv in invasions[0]:
            cog_role_id = get_cog_ping_id(inv.getCogType())
            await channel.send(
                f"# New invasion found! \n\n{inv.printOut()}\n\n<@&{cog_role_id}>"
            )
            time.sleep(0.2)  # to avoid rate limiting
    if len(invasions[1]) > 0:
        channel = bot.get_channel(1410048723743932547)
        for inv in invasions[1]:
            await channel.send(f"Ended invasion:\n{inv.printOut()}\n")


def get_cog_ping_id(cog_name: str):
    if cog_name in cog_info.cogs_role_dict:
        return cog_info.cogs_role_dict[cog_name]
    return -1


tracker = InvasionTracker()
dotenv.load_dotenv()  # Load environment variables from .env file
bot.run(os.getenv("token"))
