from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Username Required"), Length(min=4, max=15, message="username should 4 to 15 characters long")])
    name = StringField("Name", validators=[InputRequired(message="Full Name Required"), Length(min=4, max=20, message="name should be 4 to 20 characters long")])
    password = PasswordField("Password", validators=[InputRequired(message="Password Required"), EqualTo("confirm", message="Password Doesn't Match"),  Length(min=8, max=80, message="Password must contain atleast 8 characters")])
    confirm = PasswordField("Confirm Password")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Username Required"), Length(min=4, max=15, message="Incorrect Username")])
    password = PasswordField("Password", validators=[InputRequired(message="Password Required"), Length(min=8, max=80)])
