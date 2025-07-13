from googleapiclient.discovery import build
from verification import Verification
from discord import Bot, Intents, Embed
from discord.ext import tasks
import sys, os

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    sys.exit("Missing discord Token")

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
if not YOUTUBE_API_KEY:
    sys.exit("Missing YouTube API key")

YOUTUBE_ID = 1391371471254716488

intents = Intents.default()
intents.message_content = True
intents.members = True

client = Bot(intents=intents)
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def get_latest_video(channel_id):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=1
    )
    
    response = request.execute()
    video = response["items"][0]
    video_id = video["id"].get("videoId")
    
    return f"https://www.youtube.com/watch?v={video_id}" if video_id else None

@client.event
async def on_ready():
    print(f'We have successfully loggged in as {client.user} (ID: {client.user.id})')
    sys.stdout.flush()
    
    client.add_view(Verification())
    
    check_youtube.start(YOUTUBE_ID)

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

last_video_id = None

@tasks.loop(minutes=5)
async def check_youtube(youtube_id):
    global last_video_id
    
    latest_video_url = get_latest_video("UCxsZ6NCzjU_t4YSxQLBcM5A")
    if not latest_video_url:
        return
    
    video_id = latest_video_url.split("v=")[-1]
    if video_id != last_video_id:
        last_video_id = video_id
        channel = client.get_channel(youtube_id)
        await channel.send(f'Yaho! {latest_video_url}')

if __name__ == "__main__":
    client.run(TOKEN)
