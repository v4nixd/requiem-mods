from disnake import (
    AppCmdInter,
    ui,
    MediaGalleryItem,
    ButtonStyle,
    MessageInteraction,
    PartialEmoji,
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
        ticket_starter_components = [
            ui.Container(
                ui.MediaGallery(
                    MediaGalleryItem(
                        media="https://assets.rqm.bet/images/rqm-mods-nabor.png"
                    )
                ),
                ui.ActionRow(
                    ui.Button(
                        style=ButtonStyle.gray,
                        label="Подать заявку",
                        custom_id="open-mod-ticket",
                        emoji=PartialEmoji(name="openicon", id=1459973589959708867),
                    )
                ),
            )
        ]
        await inter.channel.send(components=ticket_starter_components)

    @ticket_command.error
    async def ticket_command_error(self, inter: AppCmdInter, error: Exception):
        if isinstance(error, commands.MissingPermissions):
            await inter.response.send_message(
                embed=error_embed("Недостаточно прав"), ephemeral=True
            )
            return
        await inter.response.send_message(embed=error_embed(str(error)), ephemeral=True)

    @commands.Cog.listener()
    async def on_button_click(self, inter: MessageInteraction) -> None:
        if inter.component.custom_id != "open-mod-ticket":
            return

        await inter.response.send_modal(ModTicketModal())


def setup(bot: commands.InteractionBot) -> None:
    bot.add_cog(ModTicket(bot))
