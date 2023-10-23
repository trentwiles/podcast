import requests

def getChannelVideos(apiKey, id):
    r = requests.get(f"https://www.googleapis.com/youtube/v3/search?key={apiKey}&channelId={id}&part=id&maxResults=10")
    
    videos = []

    for x in r.json()["items"]:
        if x["id"]["kind"] == "youtube#video":
            videos.append(x["id"]["videoId"])
    return videos

def getVideoMetadata(apiKey, id):
    r = requests.get(f"https://www.googleapis.com/youtube/v3/videos?key={apiKey}&id={id}&part=snippet")
    
    title = r.json()["items"][0]["snippet"]["title"]
    desc = r.json()["items"][0]["snippet"]["description"]
    thumb = r.json()["items"][0]["snippet"]["thumbnails"]["medium"]["url"]

    return {"title": title, "desc": desc, "thumbnail": thumb, "id": id}

def getChannelVideosAndData(apiKey, id):
    videos = getChannelVideos(apiKey, id)
    data = []
    for video in videos:
        data.append(getVideoMetadata(apiKey, video))
    return data