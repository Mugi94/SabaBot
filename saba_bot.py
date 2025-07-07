from verification import Verification
from discord import Bot, Intents, Embed
import sys, os

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    sys.exit("Missing discord Token.")

intents = Intents.default()
intents.message_content = True
intents.members = True

client = Bot(intents=intents)

@client.event
async def on_ready():
    print(f'We have successfully loggged in as {client.user} (ID: {client.user.id})')
    sys.stdout.flush()
    
    client.add_view(Verification())

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower() == 'paper boat':
        await message.channel.send('Paper Boat!')

@client.command()
async def setup_verifier(ctx):
    embed = Embed(
        title="Verification",
        description="Yaho!\nJoin the Kanikis!",
    )
    await ctx.channel.send(embed=embed, view=Verification())
    await ctx.respond('Verification is set up', ephemeral=True)

if __name__ == "__main__":
    client.run(TOKEN)
