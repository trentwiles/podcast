from flask import Flask, render_template, session, request, redirect
import youtube
import json
import spotify
import random
import os

app = Flask(__name__, static_url_path='/storage')
app.secret_key = json.loads(open("config.json").read())["secret"]
app.config['SESSION_TYPE'] = 'filesystem'
app.static_folder = 'storage'

@app.route('/')
def index():
    apiKey = json.loads(open("config.json").read())["youtube"]
    channel = json.loads(open("config.json").read())["channel"]
    return render_template('new.html', videos = youtube.getChannelVideosAndData(apiKey, channel), podcasts=spotify.getPodcast())

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/upload', methods=["GET"])
def login():
    return render_template('tupload.html')

@app.route('/upload', methods=["POST"])
def upload():

    password = request.form.get("password")
    if password == json.loads(open("config.json").read())["upload_password"]:
        return render_template("upload.html")
    return render_template("msg.html", msg="Incorrect Password")

@app.route('/doUpload', methods=["POST"])
def uploadFile():
    # bad code, I should be using sessions, but i'm not

    if 'file' not in request.files:
        return render_template("msg.html", msg="Missing a file")
    
    file = request.files['file']
    
    if file.filename == '':
        return render_template("msg.html", msg="Select a file!")
    
    valid = ["mp3", "wav"]
    if file.filename.split('.')[len(file.filename.split('.')) - 1] not in valid:
        return render_template("msg.html", msg=f"Bad File Extension (we accept {', '.join(valid)})")

    if file:
        filename = 'storage/' + str(random.randint(0,100000000)) + file.filename.replace(" ", "-")
        file.save(filename)
        return render_template("msg.html", msg=f"Uploaded podcast file {filename}")

if __name__ == '__main__':
    app.run(port=49385)