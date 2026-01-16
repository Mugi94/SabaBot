from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('We have successfully loggged in as %s (ID: %s)', self.bot.user, self.bot.user.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        if message.content.lower() == 'paper boat':
            await message.channel.send('Paper Boat!')
            logger.info('Paper boat sent at %s', message.channel)

def setup(bot):
    bot.add_cog(Events(bot))
