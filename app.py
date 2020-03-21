import os
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(16)
socketio = SocketIO(app)

@app.route("/")
def index():
    return "Hello World!"

if __name__ == "__main__":
    socketio.run(app)
