from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class StockForm(FlaskForm):
    music = SubmitField('Music')
    fashion = SubmitField('Fashion')
    entertainment = SubmitField('Entertainment')
    sports = SubmitField('Sports')
    technology = SubmitField('Technology')
