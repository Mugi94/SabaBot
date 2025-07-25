class YoutubeNotifier:
    def __init__(self, client, youtube, channel_id, discord_channel_id):
        self.client = client
        self.youtube = youtube
        
        self.channel = channel_id
        self.discord_channel = discord_channel_id
        
        self.last_video = None
        self.last_video_status = None

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
    
    async def check_youtube(self):
        url, status = self.get_latest_video()
        if not url:
            return
        
        video_id = url.split("v=")[-1]
        channel = self.client.get_channel(self.discord_channel)
        if video_id != self.last_video:
            self.last_video = video_id
            
            match status:
                case "upcoming":
                    await channel.send(f"Paper Boat! A stream just got planned! {url}")
                
                case "live":
                    await channel.send(f"Yaho! I'm live! {url}")
                
                case "none":
                    await channel.send(f"Yaho! {url}")
                
                case _:
                    return
        
        else:
            if self.last_video_status != status:
                if self.last_video_status == "upcoming" and status == "live":
                    await channel.send(f"Yoho! Live on! {url}")
                
                self.last_video_status = status
