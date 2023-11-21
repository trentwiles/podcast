import requests
import json

def getToken():
    api = json.loads(open("config.json").read())
    clientID = api["spotify_client_id"]
    clientSecret = api["spotify_secret"]
    r = requests.post("https://accounts.spotify.com/api/token", data={"grant_type": "client_credentials", "client_id": clientID, "client_secret": clientSecret})
    return r.json()["access_token"]

def getPodcast():
    api = json.loads(open("config.json").read())

    podcastID = api["podcastID"]
    token = getToken()

    r = requests.get(f"https://api.spotify.com/v1/shows/{podcastID}/episodes", headers={"Authorization": f"Bearer {token}"})

    podcasts = []
    for x in r.json()["items"]:
        #print(x)
        podcasts.append({"preview": x["audio_preview_url"], "link": x["external_urls"]["spotify"], "description": x["description"], "time": str(round(x['duration_ms']/1000)) + "s", "title": x["name"], "image": x["images"][0]["url"]})
    return podcasts