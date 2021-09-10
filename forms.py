from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Required


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    email = StringField('E-mail', validators=[Email()])
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

class FeedBackForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    content = StringField('Content', validators=[Required()])