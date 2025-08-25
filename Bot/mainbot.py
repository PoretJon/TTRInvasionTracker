import discord, os, dotenv
from discord import app_commands
from discord.ext import commands, tasks
from Information.CogInformation import CogInformation
from Tracker.invasion_obtainer import InvasionTracker
from Tracker.invasion import Invasion

dotenv.load_dotenv()  # Load environment variables from .env file


class TTRBot(commands.Bot):

    tracker = InvasionTracker()

    def __init__(self):
        super()
        self.bot.event(self.on_ready)

    async def on_ready(self):
        try:
            synced = await self.bot.tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)

    @bot.tree.command(name="get_invasions", description="Get current invasions")
    async def get_invasions(self, interaction: discord.Interaction):
        text = self.tracker.get_cur_invasions_message()
        await interaction.response.send_message(text)

    async def on_message(self, message):
        if message.author == self.user:  # make sure the bot doesnt reply to itself
            return

        for cog_name in CogInformation.cogs_dict:
            if cog_name.lower() in message.content.lower():
                msg = f"**Name:** {cog_name}\n**Type:** {CogInformation.cogs_dict[cog_name]}"
                await message.channel.send(msg)
                return

    @tasks.loop(minutes=5)
    async def invasion_check_loop(self):
        self.tracker.refresh_current_invasions()

    def run_bot(self):
        self.bot.run(os.getenv("token"))
