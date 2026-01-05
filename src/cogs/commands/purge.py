from disnake import AppCmdInter, DMChannel, GroupChannel, PartialMessageable, Member
from disnake.ext import commands

from src.utils import Utils


class PurgeCommand(commands.Cog):
    def __init__(self, bot: commands.InteractionBot) -> None:
        self.bot: commands.InteractionBot = bot
        print("PurgeCommand cog loaded")

    @commands.slash_command(name="purge")
    @commands.guild_only()
    async def purge(self, inter: AppCmdInter, amount: int) -> None:
        await inter.response.defer(ephemeral=True)

        channel = inter.channel

        if (
            isinstance(channel, DMChannel)
            or isinstance(channel, GroupChannel)
            or isinstance(channel, PartialMessageable)
            or not isinstance(inter.author, Member)
        ):
            await inter.edit_original_response(
                "❌ Эту команду можно использовать только на сервере"
            )
            return

        if not await Utils.is_admin(target=inter.author):
            await inter.edit_original_response("🔒 Недостаточно прав")
            return

        deleted = await channel.purge(limit=amount)

        await inter.edit_original_response(f"🧹 Удалено `{len(deleted)}` сообщений")


def setup(bot: commands.InteractionBot) -> None:
    bot.add_cog(PurgeCommand(bot))
