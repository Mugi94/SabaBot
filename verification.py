from discord.ui import View
import discord

class Verification(View):
    def __init__(self, role):
        super().__init__(timeout=None)
        self.role = role
    
    @discord.ui.button(label="Verify", custom_id="verify", style=discord.ButtonStyle.success)
    async def verify(self, button, interaction):
        user = interaction.user
        
        if self.role not in [r.id for r in user.roles]:
           await user.add_roles(user.guild.get_role(self.role))
           await interaction.response.send_message("You've been verified!", ephemeral=True)
