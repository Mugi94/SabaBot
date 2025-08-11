from googleapiclient.discovery import build
from verification import Verification
from notifier import YoutubeNotifier
from discord import Bot, Intents, Embed, Option, TextChannel
from discord.ext import tasks
import sys, os
import config

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    sys.exit("Missing discord Token")

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
if not YOUTUBE_API_KEY:
    sys.exit("Missing YouTube API key")

intents = Intents.default()
intents.message_content = True
intents.members = True

client = Bot(intents=intents)
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
notifier = YoutubeNotifier(
    client=client,
    youtube=youtube,
    channel_id="UCxsZ6NCzjU_t4YSxQLBcM5A",
    discord_channel_id=config.NOTIFICATION_CHANNEL_ID
)

@client.event
async def on_ready():
    print(f'We have successfully loggged in as {client.user} (ID: {client.user.id})')
    sys.stdout.flush()
    
    client.add_view(Verification())
    youtube_notifier.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower() == 'paper boat':
        await message.channel.send('Paper Boat!')

@client.command(name="setup", description="Where to add a verification ingetration")
async def setup_verifier(ctx, channel: Option(TextChannel, "The designed channel")):
    embed = Embed(
        title="Verification",
        description="Yaho!\nJoin the Kanikis!",
    )
    await channel.send(embed=embed, view=Verification())
    await ctx.respond('Verification is set up', ephemeral=True)

last_video_id = None

@tasks.loop(minutes=5)
async def youtube_notifier():
    await notifier.check_youtube()

if __name__ == "__main__":
    client.run(TOKEN)
