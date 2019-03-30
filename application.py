import os
import requests
from flask import Flask, session, render_template, request, url_for, jsonify, flash, abort, redirect
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
app.secret_key = "Super secret"

chatLimit = 100
rooms = {}
names = []

# C:\Users\kacey.la\AppData\Local\Programs\Python\Python37-32\Scripts
@app.route("/")
def index():
    if 'logged-in' not in session:
        session["logged-in"] = False
    return render_template("index.html")

@app.route("/username", methods=['POST'])
def usernameHandler():
    username = request.form.get('username')
    if len(username) > 10:
        flash("Username must be 10 characters or less")
    elif username not in names:
        names.append(username)
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
    return jsonify({"success": True, "channel": channel})
  
