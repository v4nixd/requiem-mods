from disnake import (
    AppCmdInter,
    ui,
    MediaGalleryItem,
    ButtonStyle,
    MessageInteraction,
    PartialEmoji,
    Member,
    File
)
from disnake.ext import commands

from src.ui.modals import ModTicketModal
from src.ui.embeds import error_embed


class ModTicket(commands.Cog):
    def __init__(self, bot: commands.InteractionBot) -> None:
        self.bot: commands.InteractionBot = bot
        print("ModTicket cog loaded")

    @commands.slash_command(name="modticket", description="test")
    @commands.has_permissions(administrator=True)
    async def ticket_command(self, inter: AppCmdInter) -> None:
        banner_file = File(
            "assets/mod_ticket_banner.png",
            filename="mod_ticket_banner.png"
        )

        ticket_starter_components = [
            ui.Container(
                ui.MediaGallery(
                    MediaGalleryItem(
                        media="attachment://mod_ticket_banner.png",
                    )
                ),
                ui.ActionRow(
                    ui.Button(
                        style=ButtonStyle.gray,
                        label="Подать заявку",
                        custom_id="open-mod-ticket",
                        emoji=PartialEmoji(
                            name="openicon", id=1459973589959708867),
                    )
                ),
            )
        ]

        author = inter.author

        if not isinstance(author, Member):
            await inter.response.send_message(embed=error_embed("Автор команды не является участником сервера"), ephemeral=True)
            return

        if not author.guild_permissions.administrator:
            await inter.response.send_message(embed=error_embed("Недостаточно прав"), ephemeral=True)
            return

        await inter.response.send_message("✅", ephemeral=True)
        await inter.channel.send(components=ticket_starter_components, file=banner_file)

    @commands.Cog.listener()
    async def on_button_click(self, inter: MessageInteraction) -> None:
        if inter.component.custom_id != "open-mod-ticket":
            return

        await inter.response.send_modal(ModTicketModal())


def setup(bot: commands.InteractionBot) -> None:
    bot.add_cog(ModTicket(bot))
