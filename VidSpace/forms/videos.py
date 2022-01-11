from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, SubmitField
from wtforms.validators import DataRequired


class UploadVideo(FlaskForm):
    video_file = FileField('Video', [DataRequired()])
    submit = SubmitField('Upload')