import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(16)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def type():
    emit("type msg", {"data": "Connected"}, broadcast=True)

@socketio.on("msg sent")
def recieve(msg):
    message = msg["message"]
    emit("msg recieve", {"message": message}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app)
