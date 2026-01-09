from disnake import AppCmdInter, Member, User, Message
from disnake.ext import commands

from src.config import Config
from src.utils import Utils


class VerifyCommand(commands.Cog):
    def __init__(self, bot: commands.InteractionBot) -> None:
        self.bot: commands.InteractionBot = bot
        self.config: Config = Config.get_instance()
        print("VerifyCommand cog loaded")

    async def verify(self, inter: AppCmdInter, target: Member) -> None:
        await inter.response.defer(ephemeral=True)

        author = inter.author

        if not isinstance(author, Member):
            return

        if not await Utils.is_admin(author):
            await inter.edit_original_response("🔒 У вас недостаточно прав")
            return

        roles_dict = self.config.get_config()["bot"]["roles"]
        autorole = target.guild.get_role(roles_dict["autorole"]["id"])
        verified_role = target.guild.get_role(roles_dict["verified"]["id"])

        if not autorole or not verified_role:
            raise ValueError("Couldn't fetch Auto role or Verified role")

        if verified_role in target.roles:
            await inter.edit_original_response(
                f"У этого пользователя уже есть роль {verified_role.mention}.\nПытаюсь забрать {autorole.mention}"
            )
            await target.remove_roles(autorole, reason=f"Verification by {author.id}")
            return

        if autorole not in target.roles:
            await inter.edit_original_response(
                f"У этого пользователя уже нету роли {autorole.mention}.\nПытаюсь выдать {verified_role.mention}"
            )
            await target.add_roles(verified_role, reason=f"Verification by {author.id}")
            return

        await target.remove_roles(autorole, reason=f"Verification by {author.id}")
        await target.add_roles(verified_role, reason=f"Verification by {author.id}")

        target = await target.guild.fetch_member(target.id)

        result_roles = [
            role for role in target.roles if role != target.guild.default_role
        ]
        result_string = "\n".join(role.mention for role in result_roles)

        await inter.edit_original_response(
            f"{target.mention} успешно верифицирован!\n\nСписок ролей пользователя:\n{result_string}"
        )

    @commands.slash_command(name="verify")
    @commands.guild_only()
    async def slash(self, inter: AppCmdInter, target: Member) -> None:
        await self.verify(inter, target)

    @commands.user_command(name="Верифицировать")
    @commands.guild_only()
    async def user(self, inter: AppCmdInter, user: User) -> None:
        if inter.guild:
            guild = inter.guild
        else:
            return

        member = await guild.fetch_member(user.id)

        if not member:
            return

        await self.verify(inter, member)

    @commands.message_command(name="Верифицировать")
    @commands.guild_only()
    async def message(self, inter: AppCmdInter, message: Message) -> None:
        author = message.author

        if not isinstance(author, Member):
            return

        await self.verify(inter, author)


def setup(bot: commands.InteractionBot) -> None:
    bot.add_cog(VerifyCommand(bot))
