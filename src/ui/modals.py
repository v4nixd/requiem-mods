from disnake import (
    ui,
    TextInputStyle,
    ModalInteraction,
    TextChannel,
    CategoryChannel,
    Member, Embed,
)

from src.config import Config
from src.utils import Utils
from src.ui.embeds import success_embed, error_embed


class ModTicketModal(ui.Modal):
    def __init__(self) -> None:
        self.config = Config.get_instance().get_config()
        self.modal_config = self.config["bot"]["modals"]["mod_ticket"]
        self.category_id = self.config["bot"]["categories"]["mod_tickets"]["id"]

        components = []
        for question in self.modal_config["questions"]:
            text_input = ui.TextInput(
                style=TextInputStyle[question["style"]],
                placeholder=question.get("placeholder"),
                required=question.get("required", True),
                custom_id=question["custom_id"],
            )
            label = ui.Label(
                text=question["label"],
                component=text_input,
            )
            components.append(label)

        super().__init__(
            title=self.modal_config["title"],
            components=components,
            timeout=self.modal_config["timeout"],
            custom_id=self.modal_config["custom_id"],
        )

    def format_answers(self, answers: dict[str, str]) -> str:
        questions = self.modal_config["questions"]
        answers_formatted = ""

        for question in questions:
            answers_formatted += (
                f"{question['label']}: `{answers[question['custom_id']]}`\n"
            )

        return answers_formatted

    async def get_category(self, inter: ModalInteraction) -> CategoryChannel:
        if not inter.guild:
            raise ValueError("Guild is None")

        category = inter.guild.get_channel(self.category_id)
        if not category or not isinstance(category, CategoryChannel):
            await inter.response.send_message("Category not found", ephemeral=True)
            raise ValueError("Category for mod tickets not found")

        return category

    async def ticket_exists_check(self, inter: ModalInteraction) -> bool:
        category = await self.get_category(inter)
        userid = inter.author.id

        if len(category.channels) > 0:
            return False

        for channel in category.channels:
            return True if str(userid) in channel.name else False
        return True

    async def create_channel(self, inter: ModalInteraction) -> tuple[TextChannel, bool]:
        if not inter.guild:
            raise ValueError("Guild is None")

        category = await self.get_category(inter)

        if not await self.ticket_exists_check(inter):
            channel = await Utils.get_channel_from_list(
                str(inter.author.id), category.channels
            )

            return channel, False

        channel = await inter.guild.create_text_channel(
            f"📦-{inter.author.id}",
            reason=f"{inter.author.id} opened a ticket",
            category=category,
            slowmode_delay=2,
        )

        if isinstance(inter.author, Member):
            author = inter.author
        else:
            raise ValueError("Author is not a member")

        ticket_init_embed = Embed(
            title=""
        )

        await channel.set_permissions(author, view_channel=True, send_messages=True)
        await channel.send(
            f"📦 {inter.author.mention} открыл тикет\n\n{self.format_answers(inter.text_values)}"
        )

        return channel, True

    async def callback(self, inter: ModalInteraction) -> None:
        channel, success = await self.create_channel(inter)
        if success:
            await inter.response.send_message(
                embed=success_embed("Тикет успешно открыт", desc=channel.mention),
                ephemeral=True,
            )
        else:
            await inter.response.send_message(
                embed=error_embed(f"У вас уже есть открытый тикет - {channel.mention}"),
                ephemeral=True,
            )
