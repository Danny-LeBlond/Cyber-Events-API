from flask_wtf import FlaskForm
from flask_wtf import RecaptchaField
from wtforms import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
import os
from flask import current_app
class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message="Enter a valid email address."),
        Length(max=100, message="Email must be under 100 characters.")
    ])
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=50, message="Name must be between 2 and 50 characters."),
        Regexp(r"^[A-Za-z\s\-']+$", message="Name can only contain letters, spaces, hyphens, or apostrophes.")
    ])
    submit = SubmitField('Confirm')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if current_app.config.get("TESTING", False):
            # Remove recaptcha field in test mode
            if 'recaptcha' in self._fields:
                del self._fields['recaptcha']
        else:
            self.recaptcha = RecaptchaField()
