from disnake.ext import commands

from src.utils import Utils


class OnConnectEvent(commands.Cog):
    def __init__(self, bot: commands.InteractionBot) -> None:
        self.bot: commands.InteractionBot = bot
        print("OnConnectEvent cog loaded")

    @commands.Cog.listener()
    async def on_connect(self) -> None:
        print(f"Connected to discord ({self.bot.user.id})")
        await Utils.update_presence(self.bot)


def setup(bot: commands.InteractionBot) -> None:
    bot.add_cog(OnConnectEvent(bot))
