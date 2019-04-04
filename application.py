import os
import requests
import datetime
from flask import Flask, session, render_template, request, url_for, jsonify, flash, abort, redirect
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
app.secret_key = "Super secret"

chatLimit = 100
channels = {}
users = []



class Channel:
    def __init__(self, name):
        self.name = name
        self.messages = []
    
    def add_message(self, m):
        self.messages.append(m)
        if len(self.messages) == 100:
            self.messages.pop()

class Message:
    def __init__(self, sender, message, date):
        self.sender = sender
        self.message = message
        self.date = date

# C:\Users\kacey.la\AppData\Local\Programs\Python\Python37-32\Scripts
@app.route("/")
def index():
    if 'logged-in' not in session:
        session["logged-in"] = False

    return render_template("index.html", channels = channels)

@app.route("/username", methods=['POST'])
def usernameHandler():
    username = request.form.get('username')
    if len(username) > 10:
        flash("Username must be 10 characters or less")
    elif username not in users:
        users.append(username)
        session["logged-in"] = True
        session["username"] = username
        flash("You may start chatting!")        
    else:
        flash("Sorry, this username is already taken")
    return redirect(url_for('index'))
  
@socketio.on('create channel')
def createChannel(data):
    channel = data["channel"]

    if len(channel) > 10:
        return False
    elif channel in channels:
        return False

    channels[channel] = Channel(channel)
    emit("add channel", channel, broadcast=True)

@socketio.on('store message')
def storeMessage(data):
    message, sender, date, channel = data["message"], data["sender"], data["date"], data["channel"]
    channelMessage = Message(message, sender, date)
    # channels[channel].addMessage(channelMessage)
    emit("send message", data, broadcast=True)