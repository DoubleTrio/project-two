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
    
    def print_info(self):
        print(f"Channel name: {self.name}")
        print()
        print("Messages:")
        for message in self.messages:
            print(message.sender, message.message)

class Message:
    def __init__(self, sender, message, date, time):
        self.sender = sender
        self.message = message
        self.date = date
        self.time = time

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

@app.route("/message", methods=['POST'])
def sendMessage():
    message = request.form.get('message')

    if message:
        flash(f"Send this data: {message}")
    if message == "logout":
        session.clear()
    return redirect(url_for('index'))


@app.route("/channel", methods=['POST'])
def createChannel():
    channel = request.form.get('channel')
    return 'r'

#     if len(channel) > 10:
#         return jsonify({"success": False, "error": "Channels must be 10 characters or less"})
#     elif channel in channels:
#         return jsonify({"success": False, "error": "Sorry, the channel is already made"})
    
#     channels[channel] = Channel(channel)
#     return jsonify({"success": True, "channel": channel})
  
@socketio.on('create channel')
def CreateChannel(data):
    channel = data["channel"]
    if len(channel) > 10:
        return False
    elif channel in channels:
        return False
    channels[channel] = Channel(channel)
    emit("add channel", channel, broadcast=True)

@socketio.on('store message')
def storeMessage(data):
    message, sender, date, time, channel = data["message"], data["sender"], data["date"], data["time"], data["channel"]
    channelMessage = Message(message, sender, date, time)
    # channels[channel].append(channelMessage)
    emit("send message", data, broadcast=True)