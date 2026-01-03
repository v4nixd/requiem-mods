from disnake.ext import commands


class OnDisconnectEvent(commands.Cog):
    def __init__(self, bot: commands.InteractionBot) -> None:
        self.bot: commands.InteractionBot = bot
        print("OnDisconnectEvent cog loaded")

    @commands.Cog.listener()
    async def on_disconnect(self) -> None:
        print("Lost connection from discord")


def setup(bot: commands.InteractionBot) -> None:
    bot.add_cog(OnDisconnectEvent(bot))
