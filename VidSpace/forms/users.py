from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Email, ValidationError
from VidSpace import mysql


class Signup(FlaskForm):
    first_name = StringField("First Name", [Length(min=3, max=30), DataRequired()])
    last_name = StringField("Last Name", [Length(min=3, max=30), DataRequired()])
    email = StringField("Email", [Email(), DataRequired()])
    password = PasswordField("Password", [Length(min=6, max=30), EqualTo('confirm_password', message="Password do not match!"), DataRequired()])
    confirm_password = PasswordField("Confirm Password")
    phone = StringField("Phone Number", [Length(min=10, max=12), DataRequired()])
    submit = SubmitField("Sign up")

    def validate_email(self, email):
        cur = mysql.connection.cursor()
        result = cur.execute('''SELECT * FROM users WHERE email = %s''', [email.data])

        if result > 0:
            raise ValidationError("This email has been already registered!")


    def validate_phone(self, phone):
        cur = mysql.connection.cursor()
        result = cur.execute('''SELECT * FROM users WHERE phone = %s''', [phone.data])

        if result > 0:
            raise ValidationError("This phone number has been already registered!")