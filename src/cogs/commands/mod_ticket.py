from disnake import AppCmdInter
from disnake.ext import commands

from src.ui.modals import ModTicketModal

class ModTicket(commands.Cog):
    def __init__(self, bot: commands.InteractionBot) -> None:
        self.bot: commands.InteractionBot = bot
        print("ModTicket cog loaded")

    @commands.slash_command(name="modticket", description="test")
    async def ticket_command(self, inter: AppCmdInter) -> None:
        modal = ModTicketModal()

        await inter.response.send_modal(modal)

def setup(bot: commands.InteractionBot) -> None:
    bot.add_cog(ModTicket(bot))