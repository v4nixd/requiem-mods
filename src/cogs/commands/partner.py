from disnake import AppCmdInter, Member, User, Message
from disnake.ext import commands

from src.config import Config
from src.utils import Utils


class PartnerCommand(commands.Cog):
    def __init__(self, bot: commands.InteractionBot) -> None:
        self.bot: commands.InteractionBot = bot
        self.config: Config = Config.get_instance()
        print("PartnerCommand cog loaded")

    async def partner(self, inter: AppCmdInter, target: Member) -> None:
        await inter.response.defer(ephemeral=True)

        author = inter.author

        if not isinstance(author, Member):
            return

        if not await Utils.is_admin(author):
            await inter.edit_original_response("🔒 У вас недостаточно прав")
            return

        roles_dict = self.config.get_config()["bot"]["roles"]

        partner = target.guild.get_role(roles_dict["partner"]["id"])

        if not partner:
            raise ValueError("Couldn't fetch Partner role")

        if partner in target.roles:
            await inter.edit_original_response(
                f"У этого пользователя уже есть роль {partner.mention}"
            )
            return

        await target.add_roles(partner, reason=f"Partner verification by {author.id}")

        target = await target.guild.fetch_member(target.id)

        result_roles = [
            role for role in target.roles if role != target.guild.default_role
        ]
        result_string = "\n".join(role.mention for role in result_roles)

        await inter.edit_original_response(
            f"{target.mention} теперь наш партнер\n\nСписок ролей пользователя:\n{result_string}"
        )

    @commands.slash_command(name="partner")
    @commands.guild_only()
    async def slash(self, inter: AppCmdInter, target: Member) -> None:
        await self.partner(inter, target)

    @commands.user_command(name="Сделать партнером")
    @commands.guild_only()
    async def user(self, inter: AppCmdInter, user: User) -> None:
        if inter.guild:
            guild = inter.guild
        else:
            return

        member = await guild.fetch_member(user.id)

        if not member:
            return

        await self.partner(inter, member)

    @commands.message_command(name="Сделать партнером")
    @commands.guild_only()
    async def message(self, inter: AppCmdInter, message: Message) -> None:
        author = message.author

        if not isinstance(author, Member):
            return

        await self.partner(inter, author)


def setup(bot: commands.InteractionBot) -> None:
    bot.add_cog(PartnerCommand(bot))
