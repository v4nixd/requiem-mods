from disnake import Activity, ActivityType, Status, Member, User, Guild
from disnake.ext import commands

from src.config import Config


class Utils:
    @staticmethod
    def load_cogs(bot: commands.InteractionBot) -> None:
        print("Loading cogs")
        bot.load_extensions("src/cogs/events")
        bot.load_extensions("src/cogs/commands")
        print("Cogs loaded")

    @staticmethod
    async def update_presence(bot: commands.InteractionBot) -> None:
        config = Config.get_instance().get_config()
        activity = config["bot"]["activity"]

        await bot.change_presence(
            activity=Activity(
                type=ActivityType[activity["type"]], name=activity["name"]
            ),
            status=Status[activity["status"]],
        )

    @staticmethod
    async def is_admin(target: Member) -> bool:
        roles_dict = Config.get_instance().get_config()["bot"]["roles"]

        owner_role = await target.guild.fetch_role(roles_dict["owner"]["id"])
        admin_role = await target.guild.fetch_role(roles_dict["admin"]["id"])
        trusted_role = await target.guild.fetch_role(roles_dict["trusted"]["id"])
        moderator_role = await target.guild.fetch_role(roles_dict["moderator"]["id"])

        roles_list = [owner_role, admin_role, trusted_role, moderator_role]
        roles_count = 0

        for role in roles_list:
            if role in target.roles:
                roles_count += 1
                break

        return roles_count > 0

    @staticmethod
    def is_member(target: User | Member) -> bool:
        if isinstance(target, Member):
            return True
        else:
            return False

    @staticmethod
    async def get_guild(bot: commands.InteractionBot) -> Guild:
        return bot.get_guild(Config.get_instance().get_config()["bot"]["server"]["id"])
