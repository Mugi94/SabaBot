from discord import Bot, Intents
import sys, os

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    sys.exit("Le token Discord est manquant.")

intents = Intents.default()
intents.message_content = True

client = Bot(intents=intents)

@client.event
async def on_ready():
    print(f'We have successfully loggged in as {client.user} (ID: {client.user.id})')
    sys.stdout.flush()

if __name__ == "__main__":
    client.run(TOKEN)
