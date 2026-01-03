# EXAMPLE COMMAND
from disnake import AppCmdInter, DMChannel, GroupChannel, PartialMessageable, Member, DiscordException
from disnake.ext import commands

from src.config import Config


class PurgeCommand(commands.Cog):
    def __init__(self, bot: commands.InteractionBot) -> None:
        self.bot: commands.InteractionBot = bot
        self.config: Config = Config.get_instance()
        print("PurgeCommand cog loaded")

    @commands.slash_command(name="purge")
    @commands.guild_only()
    async def purge(self, inter: AppCmdInter, amount: int) -> None:
        await inter.response.defer(ephemeral=True)

        config = self.config.get_config()
        admin_role_id = config["bot"]["roles"]["admin"]["id"]

        channel = inter.channel

        if (
            isinstance(channel, DMChannel)
            or isinstance(channel, GroupChannel)
            or isinstance(channel, PartialMessageable)
            or not isinstance(inter.author, Member)
        ):
            await inter.edit_original_response(
                "❌ You can only use this command in guilds"
            )
            return

        if not inter.author.get_role(admin_role_id):
            await inter.edit_original_response(
                "❌ Insufficient permissions"
            )
            return

        deleted = await channel.purge(limit=amount)

        await inter.edit_original_response(f"🧹 Purged `{len(deleted)}` messages")


def setup(bot: commands.InteractionBot) -> None:
    bot.add_cog(PurgeCommand(bot))
