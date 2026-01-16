from discord import Bot, Intents
import logging
import logging.config
import sys, os, json

# Logger configuration
os.makedirs("logs", exist_ok=True)

with open('./logging.json') as config_file:
    config = json.load(config_file)

logging.config.dictConfig(config)
logger = logging.getLogger("SabaBot")

# Bot configuration
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    logger.critical("Missing discord Token")
    sys.exit(1)

intents = Intents.default()
intents.message_content = True
intents.members = True

client = Bot(intents=intents)

for extension in ['events', 'notifier']:
    try:
        client.load_extension(f'cogs.{extension}')
        logger.info("Extension loaded: cogs.%s", extension)
    except Exception as err:
        logger.exception("Error while loading extension")

if __name__ == "__main__":
    client.run(TOKEN)
