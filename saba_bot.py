from discord import Bot, Intents
import logging
import sys, os
    
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    handlers=[
        logging.FileHandler('logs/discord.log', encoding='utf-8', mode='w'),
        logging.StreamHandler()
    ]
)

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    logging.error("Missing discord Token")
    sys.exit(1)

intents = Intents.default()
intents.message_content = True
intents.members = True

client = Bot(intents=intents)

for extension in ['events', 'notifier']:
    try:
        client.load_extension(f'cogs.{extension}')
        logging.info(f"Extension loaded: cogs.%s", extension)
    except Exception as err:
        logging.exception(f"Error while loading extension: %s", err)

if __name__ == "__main__":
    client.run(TOKEN)
