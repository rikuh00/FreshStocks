from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class StockForm(FlaskForm):
    interests = SubmitField('Interests')
    home = SubmitField('Home')

