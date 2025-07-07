from discord.ui import View
import discord

class Verification(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Verify", custom_id="verify", style=discord.ButtonStyle.success)
    async def verify(self, button, interaction):
        role_id = 1391525958715969616
        user = interaction.user
        
        if role_id not in [r.id for r in user.roles]:
           await user.add_roles(user.guild.get_role(role_id))
           await interaction.response.send_message("You've been verified!", ephemeral=True)
