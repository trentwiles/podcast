from flask import Flask, render_template, session, request
import youtube
import json
import spotify
import random

app = Flask(__name__)
app.secret_key = json.loads(open("config.json").read())["secret"]

@app.route('/')
def index():
    apiKey = json.loads(open("config.json").read())["youtube"]
    channel = json.loads(open("config.json").read())["channel"]
    return render_template('index.html', videos = youtube.getChannelVideosAndData(apiKey, channel), podcasts=spotify.getPodcast())

@app.route('/upload')
def upload():
    try:
        if session['isLoggedIn'] != True:
            return render_template("login.html")
        return render_template('upload.html')
    except:
        return render_template('upload.html')

@app.route('/doUpload', methods=["POST"])
def uploadFile():
    if 'file' not in request.files:
        return render_template("msg.html", msg="Missing a file")
    
    file = request.files['file']
    
    if file.filename == '':
        return render_template("msg.html", msg="Select a file!")
    
    valid = ["mp3", "wav", "aac", "ogg"]
    if file.filename.split('.')[len(file.filename.split('.')) - 1] not in valid:
        return render_template("msg.html", msg=f"Bad File Extension (we accept {', '.join(valid)})")

    if file:
        filename = 'storage/' + str(random.randint(0,100000000)) + file.filename.replace(" ", "-")
        file.save(filename)
        return render_template("msg.html", msg=f"Uploaded podcast file {filename}")


if __name__ == '__main__':
    app.run(debug=True)