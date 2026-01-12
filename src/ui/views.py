import time
import asyncio

from disnake import (
    ui,
    ButtonStyle,
    MessageInteraction,
    Member,
    Embed,
    TextChannel,
    PartialEmoji,
)

from src.ui.embeds import error_embed, success_embed
from src.config import Config


class ModTicketControlsView(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    async def check_perms(self, inter: MessageInteraction) -> bool:
        config = Config.get_instance().get_config()
        roles = config["bot"]["roles"]

        admin_roles_json = roles["owner"], roles["dep_owner"]
        admin_roles = []

        guild = inter.guild
        author = inter.author

        if not isinstance(author, Member):
            raise ValueError("Author is not a member")

        if not guild:
            raise ValueError("Guild not found in inter ", inter)

        for json_role in admin_roles_json:
            admin_roles.append(guild.get_role(int(json_role["id"])))

        roles_count = 0
        for role in admin_roles:
            if role in author.roles:
                roles_count += 1
        if roles_count <= 0:
            await inter.response.send_message(
                embed=error_embed("У вас недостаточно прав!"), ephemeral=True
            )
            return False  # not enough perms, fail
        else:
            return True  # enough perms, success

    async def get_issuer(self, inter: MessageInteraction) -> tuple[Member | None, str]:
        channel = inter.channel

        if not isinstance(channel, TextChannel):
            raise ValueError("Channel is not a TextChannel")
        if not channel:
            raise ValueError("Channel not found in inter ", inter)

        ticket_issuer_id = channel.name.split("-")[1]
        guild = inter.guild
        if not guild:
            raise ValueError("Guild not found in inter ", inter)
        return guild.get_member(int(ticket_issuer_id)), ticket_issuer_id

    @ui.button(
        style=ButtonStyle.gray, custom_id="mod-ticket-close", emoji=PartialEmoji(name="close", id=1459986490737295622), label="Закрыть"
    )
    async def close_ticket(self, button: ui.Button, inter: MessageInteraction) -> None:
        if not await self.check_perms(inter):
            return

        ticket_issuer, ticket_issuer_id = await self.get_issuer(inter)

        if not ticket_issuer:
            await inter.response.send_message(
                embed=error_embed(
                    f"Не получилось найти участника с айди {ticket_issuer_id}"
                ),
                ephemeral=True,
            )
            return

        channel = inter.channel
        guild = inter.guild

        if not guild:
            raise ValueError("Guild not found in inter ", inter)

        if not isinstance(channel, TextChannel):
            raise ValueError("Channel is not a TextChannel")
        if not channel:
            raise ValueError("Channel not found in inter ", inter)

        await channel.set_permissions(
            target=ticket_issuer,
            view_channel=False,
            send_messages=False,
            reason=f"Ticket closed by {inter.author.id}",
        )
        await channel.set_permissions(
            target=guild.default_role,
            view_channel=False,
            send_messages=False,
            reason=f"Ticket closed by {inter.author.id}",
        )

        await inter.response.send_message(embed=success_embed("Тикет успешно закрыт"))

    @ui.button(
        style=ButtonStyle.red, custom_id="mod-ticket-delete", emoji=PartialEmoji(name="trash", id=1459986489088675900), label="Удалить"
    )
    async def delete_ticket(self, button: ui.Button, inter: MessageInteraction) -> None:
        if not await self.check_perms(inter):
            return

        ticket_issuer, ticket_issuer_id = await self.get_issuer(inter)

        channel = inter.channel

        if not isinstance(channel, TextChannel):
            raise ValueError("Channel is not a TextChannel")
        if not channel:
            raise ValueError("Channel not found in inter ", inter)

        if not ticket_issuer:
            await inter.response.send_message(
                embed=error_embed(
                    f"Не получилось найти участника с айди {ticket_issuer_id}"
                ),
                ephemeral=True,
            )
            return

        await inter.response.send_message(
            embed=success_embed("Тикет будет удален в течении 5 секунд"), ephemeral=True
        )
        await asyncio.sleep(5)
        await channel.delete(reason=f"Ticket deleted by {inter.author.id}")

    @ui.button(
        style=ButtonStyle.gray,
        custom_id="mod-ticket-archive",
        emoji=PartialEmoji(name="archive", id=1459986487360622624),
        label="Архивировать",
    )
    async def archive_ticket(
        self, button: ui.Button, inter: MessageInteraction
    ) -> None:
        if not await self.check_perms(inter):
            return

        ticket_issuer, ticket_issuer_id = await self.get_issuer(inter)

        if not ticket_issuer:
            await inter.response.send_message(
                embed=error_embed(
                    f"Не получилось найти участника с айди {ticket_issuer_id}"
                ),
                ephemeral=True,
            )
            return

        guild = inter.guild
        if not guild:
            raise ValueError("Guild not found in inter ", inter)

        channel = inter.channel

        if not isinstance(channel, TextChannel):
            raise ValueError("Channel is not a TextChannel")

        config = Config.get_instance().get_config()
        archive_category_id = config["bot"]["categories"]["archive_mod_tickets"]["id"]
        archive_category = guild.get_channel(int(archive_category_id))
        archive_time = int(time.time())

        archive_emoji = "<:archive:1459986487360622624>"
        user_emoji = "<:user:1459985193535406284>"
        time_emoji = "<:time:1460063328519979259>"

        await channel.edit(
            category=archive_category, reason=f"Ticket archive by {inter.author.id}"
        )
        await channel.send(
            embed=Embed(
                title=f"{archive_emoji} Тикет был архивирован",
                description=f"{user_emoji} **Инициатор** : {inter.author.mention}\n{time_emoji} **Время** : <t:{archive_time}:F>",
            )
        )
        await inter.response.send_message(
            embed=success_embed("Тикет успешно архивирован"), ephemeral=True
        )
