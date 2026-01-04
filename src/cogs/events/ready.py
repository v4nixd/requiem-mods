from disnake import Guild
from disnake.ext import commands, tasks

from src.config import Config


class OnReadyEvent(commands.Cog):
    def __init__(self, bot: commands.InteractionBot) -> None:
        self.bot: commands.InteractionBot = bot
        self.config: Config = Config.get_instance()
        print("OnReadyEvent cog loaded")

    async def get_guild(self, config) -> Guild:
        guild = self.bot.get_guild(config["bot"]["server"]["id"])

        if not guild:
            raise ValueError("Couldn't get guild")

        return guild

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Bot ready")

        if not self.server_stats.is_running():
            self.server_stats.start()

    @tasks.loop(seconds=10)
    async def server_stats(self) -> None:
        config = self.config.get_config()

        guild = await self.get_guild(config)
        channel = guild.get_channel(
            config["bot"]["channels"]["stats_membercount"]["id"]
        )

        if not channel:
            raise ValueError("Stats Member count channel not found")

        template = str(config["bot"]["channels"]["stats_membercount"]["template"])

        await channel.edit(name=template.format(count=guild.member_count))


def setup(bot: commands.InteractionBot) -> None:
    bot.add_cog(OnReadyEvent(bot))
