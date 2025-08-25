import os, discord, dotenv
from discord.ext import commands, tasks
from Information import CogInformation
from Tracker.invasion import Invasion
from Tracker.invasion_obtainer import InvasionTracker

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


@bot.tree.command(
    name="refresh_invasions",
    description="Refresh invasions",
    guild=discord.Object(id=975230586635550831),
)
async def refresh_invasions(interaction):
    tracker.refresh_current_invasions()
    await interaction.response.send_message("Invasions refreshed.")


async def on_message(message):
    if message.author == bot.user:  # make sure the bot doesnt reply to itself
        return

    for cog_name in CogInformation.cogs_dict:
        if cog_name.lower() in message.content.lower():
            msg = (
                f"**Name:** {cog_name}\n**Type:** {CogInformation.cogs_dict[cog_name]}"
            )
            await message.channel.send(msg)
            return


@tasks.loop(minutes=5)
async def invasion_check_loop():
    tracker.refresh_current_invasions()


tracker = InvasionTracker()
dotenv.load_dotenv()  # Load environment variables from .env file
bot.run(os.getenv("token"))
