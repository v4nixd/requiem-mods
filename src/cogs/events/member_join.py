from disnake import Member
from disnake.ext import commands

from src.config import Config


class OnMemberJoin(commands.Cog):
    def __init__(self, bot: commands.InteractionBot) -> None:
        self.bot: commands.InteractionBot = bot
        self.config: Config = Config.get_instance()
        print("OnMemberJoin cog loaded")

    @commands.Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        role_id = self.config.get_config()["bot"]["roles"]["autorole"]["id"]

        role = member.guild.get_role(role_id)
        if not role:
            raise ValueError(f"Role with ID ({role_id}) not found")

        await member.add_roles(role, reason="Autorole")


def setup(bot: commands.InteractionBot) -> None:
    bot.add_cog(OnMemberJoin(bot))
