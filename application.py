import os
import requests
import json
from flask import Flask, session, render_template, request, url_for, jsonify, flash, abort, redirect
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
app.secret_key = "Super secret, don't tell uwu"
# C:\Users\kacey.la\AppData\Local\Programs\Python\Python37-32\Scripts

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

channels = {"General": Channel("General")}
users = []

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'logged-in' not in session:
        session["logged-in"] = False
    if 'last-channel' not in session:
         session["last-channel"] = "General"
    currentChannelList = []
    for channel in channels:
        currentChannelList.append(channels[channel].name)
    messages = channels[session["last-channel"]].messages
    return render_template("index.html", channels = currentChannelList, messages = messages, channelName = session["last-channel"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/username", methods=['POST'])
def usernameHandler():
    username = request.form.get('username')
    if len(username) > 10:
        flash("Username must be 10 characters or less")
    elif username not in users:
        users.append(username)
        session["logged-in"] = True
        session["username"] = username
    else:
        flash("Sorry, this username is already taken")
    return redirect(url_for('index'))

@app.route("/channel/<string:channel>")
def visitChannel(channel):

    return channel

@app.route("/channel")
def changeChannel():

    return "Hallo"
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
    channelMessage = Message(sender, message, date)
    channels[channel].add_message(channelMessage)
    emit("send message", data, broadcast=True)