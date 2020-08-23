from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class WelcomeForm(FlaskForm):
    cash = FloatField('Available Cash', validators=[DataRequired()])
    submit = SubmitField('Start Investing!')
