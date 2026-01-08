from disnake import ui, TextInputStyle, ModalInteraction, CategoryChannel

from src.config import Config

class ModTicketModal(ui.Modal):
    def __init__(self) -> None:
        self.config = Config.get_instance().get_config()
        self.modal_config = Config.get_instance().get_config()["bot"]["modals"]["mod_ticket"]
        self.category_id = Config.get_instance().get_config()["bot"]["categories"]["mod_tickets"]["id"]

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
            custom_id=self.modal_config["custom_id"]
        )

    async def callback(self, inter: ModalInteraction) -> None:
        questions = self.modal_config["questions"]
        answers = inter.text_values

        answers_formatted = ""

        for question in questions:
            answers_formatted += f"{question['label']}: `{answers[question["custom_id"]]}`\n"

        category = inter.guild.get_channel(self.category_id)
        if not category or not isinstance(category, CategoryChannel):
            await inter.response.send_message("Category not found", ephemeral=True)
            return

        channel = await inter.guild.create_text_channel(f"📦-{inter.author.id}", reason=f"{inter.author.id} opened a ticket", category=category, slowmode_delay=2)
        await channel.set_permissions(inter.author, view_channel=True, send_messages=True)
        await channel.send(f"📦 {inter.author.mention} открыл тикет\n\n{answers_formatted}")
        await inter.response.send_message(f"📦 Тикет успешно открыт - {channel.mention}", ephemeral=True)