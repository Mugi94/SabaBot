from discord import Bot, Intents
import sys, os

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    sys.exit("Missing discord Token")

intents = Intents.default()
intents.message_content = True
intents.members = True

client = Bot(intents=intents)

for extension in ['events', 'notifier']:
    try:
        client.load_extension(f'cogs.{extension}')
    except Exception as err:
        print(err)

if __name__ == "__main__":
    client.run(TOKEN)
