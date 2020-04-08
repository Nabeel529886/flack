import os
from time import strftime, localtime
from flask import Flask, render_template, flash, redirect, url_for
from form_fields import RegisterForm, LoginForm
from flask_bootstrap import Bootstrap
from passlib.hash import sha256_crypt
from models import *
from flask_socketio import SocketIO, send, join_room, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(14)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

socketio = SocketIO(app)

Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


ROOMS = ["Electromates", "Programming"]

@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if sha256_crypt.verify(form.password.data, user.password):
                login_user(user)
                flash("Successfully Logged In", "success")
                return redirect(url_for("chat"))
            else:
                flash("Incorrect username or Password", "danger")
        else:
            flash("No User by that Username", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        user_check = User.query.filter_by(username=username).first()
        if user_check:
            flash("Username Already Taken", "danger")
        else:
            name = form.name.data
            password = form.password.data
            hashed_pswd = sha256_crypt.hash(password)
            user = User(username=username, name=name, password=hashed_pswd)
            db.session.add(user)
            db.session.commit()
            flash("User Registered Successfully", "success")
            return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html", rooms=ROOMS)


@socketio.on("incoming-msg")
def incoming_msg(data):
    msg = data["msg"]
    username = data["username"]
    time_stamp = strftime("%b %d %Y, %I:%M:%S %p", localtime())
    room = data["room"]
    send({"msg": msg, "username": username, "name": current_user.name, "time_stamp": time_stamp}, room=room)

@socketio.on("join")
def join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)
    send({"msg": username + " has joined the " + room + " room."}, room=room)

@socketio.on("leave")
def leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " has left the room"}, room=room)




if __name__ == "__main__":
    socketio.run(app)
