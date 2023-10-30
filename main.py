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
    if session['isLoggedIn'] != True:
        return render_template("login.html")
    return render_template('upload.html')

@app.route('/doUpload')
def uploadFile():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    if file.filename.split('.')[len(file.filename.split('.')) - 1] not in ["mp3", "wav", "aac", "ogg"]:
        return 'Bad file ext'

    if file:
        filename = str(random.randint(0,100000000)) + file.filename
        file.save(filename)
        return 'File successfully uploaded! ' + filename


if __name__ == '__main__':
    app.run(debug=True)