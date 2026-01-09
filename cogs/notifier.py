from googleapiclient.discovery import build
from discord.ext import commands, tasks
import config
import sys, os

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
if not YOUTUBE_API_KEY:
    sys.exit("Missing YouTube API key")

class YoutubeNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        
        self.channel = config.YOUTUBE_CHANNEL_ID
        self.discord_channel = config.NOTIFICATION_CHANNEL_ID
        
        self.last_video = None
        self.last_video_status = None
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.check_youtube.start()

    def get_latest_video(self):
        request = self.youtube.search().list(
            part="snippet",
            channelId=self.channel,
            order="date",
            maxResults=1
        )
        
        response = request.execute()
        video = response["items"][0]
        video_id = video["id"].get("videoId")
        
        status = video["snippet"].get("liveBroadcastContent")
        if video_id and status:
            return f"https://www.youtube.com/watch?v={video_id}", status
        
        return None, None
    
    @tasks.loop(minutes=5)
    async def check_youtube(self):
        url, status = self.get_latest_video()
        if not url:
            return
        
        video_id = url.split("v=")[-1]
        channel = self.bot.get_channel(self.discord_channel)
        if video_id != self.last_video:
            self.last_video = video_id
            text = f"<@&{config.NOTIFICATION_ROLE_ID}> "
            
            match status:
                case "upcoming":
                    await channel.send(f"{text} Paper Boat! A stream just got planned! {url}")
                
                case "live":
                    await channel.send(f"{text} Yaho! I'm live! {url}")
                
                case "none":
                    await channel.send(f"{text} Yaho! {url}")
                
                case _:
                    return
        
        else:
            if self.last_video_status != status:
                if self.last_video_status == "upcoming" and status == "live":
                    await channel.send(f"Yoho! Live on! {url}")
                
                self.last_video_status = status
                
def setup(bot):
    bot.add_cog(YoutubeNotifier(bot))
