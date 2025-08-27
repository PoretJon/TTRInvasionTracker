import os, discord, dotenv
from discord.ext import commands, tasks
from Information import CogInformation
from Tracker.invasion import Invasion
from Tracker.invasion_obtainer import InvasionTracker
import time


cog_info = CogInformation.CogInformation()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
# tree = discord.app_commands.CommandTree(bot)


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


# not to be used in production
# @bot.tree.command(
#     name="refresh_invasions",
#     description="Refresh invasions",
#     guild=discord.Object(id=975230586635550831),
# )
# async def refresh_invasions(interaction):
#     invasions = tracker.refresh_current_invasions()
#     await interaction.response.send_message("Invasions refreshed.")
#     if len(invasions[0]) > 0:  # there are new invasions
#         print("new invasions")
#         for inv in invasions[0]:
#             await interaction.followup.send(f"New invasion:\n{inv.printOut()}\n")
#     if len(invasions[1]) > 0:  # there are ended invasions
#         print("ended invasions")
#         for inv in invasions[1]:
#             await interaction.followup.send(f"Ended invasion:\n{inv.printOut()}\n")


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
