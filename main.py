from flask import Flask, render_template
import youtube
import json
import spotify

app = Flask(__name__)

@app.route('/')
def index():
    apiKey = json.loads(open("config.json").read())["youtube"]
    channel = json.loads(open("config.json").read())["channel"]
    return render_template('index.html', videos = youtube.getChannelVideosAndData(apiKey, channel), podcasts=spotify.getPodcast())

if __name__ == '__main__':
    app.run(debug=True)