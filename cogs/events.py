from discord.ext import commands
import sys

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have successfully loggged in as {self.bot.user} (ID: {self.bot.user.id})')
        sys.stdout.flush()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        if message.content.lower() == 'paper boat':
            await message.channel.send('Paper Boat!')

def setup(bot):
    bot.add_cog(Events(bot))
