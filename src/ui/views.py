import time
import asyncio

from disnake import ui, ButtonStyle, MessageInteraction, Member, User, Embed

from src.ui.embeds import error_embed, success_embed
from src.config import Config


class ModTicketView(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @ui.button(
        style=ButtonStyle.green,
        custom_id="mod-ticket-open",
        emoji="📩",
        label="Открыть тикет",
    )
    async def open_ticket(self, button: ui.Button, inter: MessageInteraction) -> None:
        from src.ui.modals import ModTicketModal
        await inter.response.send_modal(ModTicketModal())

class ModTicketControlsView(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    async def check_perms(self, inter: MessageInteraction) -> bool:
        config = Config.get_instance().get_config()
        roles = config["bot"]["roles"]

        admin_roles_json = roles["owner"], roles["dep_owner"]
        admin_roles = []

        for json_role in admin_roles_json:
            admin_roles.append(inter.guild.get_role(int(json_role["id"])))

        print(admin_roles)

        roles_count = 0
        for role in admin_roles:
            if role in inter.author.roles:
                print(role, "in", inter.author)
                roles_count += 1
                print(roles_count)
            else:
                print(role, "out", inter.author)
        if roles_count <= 0:
            print(roles_count, "not enough roles")
            await inter.response.send_message(
                embed=error_embed("У вас недостаточно прав!"), ephemeral=True
            )
            return False # not enough perms, fail
        else:
            print("enough roles", roles_count)
            return True # enough perms, success

    async def get_issuer(self, inter: MessageInteraction) -> tuple[Member | None, str]:
        ticket_issuer_id = inter.channel.name.split("-")[1]
        return inter.guild.get_member(int(ticket_issuer_id)), ticket_issuer_id

    @ui.button(
        style=ButtonStyle.red,
        custom_id="mod-ticket-close",
        emoji="🔒",
        label="Закрыть"
    )
    async def close_ticket(self, button: ui.Button, inter: MessageInteraction) -> None:
        if not await self.check_perms(inter): return

        ticket_issuer, ticket_issuer_id = await self.get_issuer(inter)

        if not ticket_issuer:
            await inter.response.send_message(embed=error_embed(f"Не получилось найти участника с айди {ticket_issuer_id}"), ephemeral=True)
            return

        await inter.channel.set_permissions(target=ticket_issuer, view_channel=False, send_messages=False, reason=f"Ticket closed by {inter.author.id}")
        await inter.channel.set_permissions(target=inter.guild.default_role, view_channel=False, send_messages=False, reason=f"Ticket closed by {inter.author.id}")

        await inter.response.send_message(embed=success_embed("Тикет успешно закрыт"))

    @ui.button(
        style=ButtonStyle.red,
        custom_id="mod-ticket-delete",
        emoji="🗑️",
        label="Удалить"
    )
    async def delete_ticket(self, button: ui.Button, inter: MessageInteraction) -> None:
        if not await self.check_perms(inter): return

        ticket_issuer, ticket_issuer_id = await self.get_issuer(inter)

        if not ticket_issuer:
            await inter.response.send_message(embed=error_embed(f"Не получилось найти участника с айди {ticket_issuer_id}"), ephemeral=True)
            return

        await inter.response.send_message(embed=success_embed("Тикет будет удален в течении 5 секунд"), ephemeral=True)
        await asyncio.sleep(5)
        await inter.channel.delete(reason=f"Ticket deleted by {inter.author.id}")

    @ui.button(
        style=ButtonStyle.gray,
        custom_id="mod-ticket-archive",
        emoji="🗃️",
        label="Архивировать"
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

        config = Config.get_instance().get_config()
        archive_category_id = config["bot"]["categories"]["archive_mod_tickets"]["id"]
        archive_category = inter.guild.get_channel(int(archive_category_id))
        archive_time = int(time.time())

        await inter.channel.edit(category=archive_category, reason=f"Ticket archive by {inter.author.id}")
        await inter.channel.send(embed=Embed(title="🗃️ Тикет был архивирован", description=f"👤 **Инициатор** : {inter.author.mention}\n🕒 **Время** : <t:{archive_time}:F>"))
        await inter.response.send_message(embed=success_embed("Тикет успешно архивирован"), ephemeral=True)