from disnake.ext import commands


class OnResumedEvent(commands.Cog):
    def __init__(self, bot: commands.InteractionBot) -> None:
        self.bot: commands.InteractionBot = bot
        print("OnResumedEvent cog loaded")

    @commands.Cog.listener()
    async def on_resumed(self) -> None:
        print("Re-established connection with discord")


def setup(bot: commands.InteractionBot) -> None:
    bot.add_cog(OnResumedEvent(bot))
