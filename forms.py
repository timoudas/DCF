from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length

class TickerForm(FlaskForm):
	ticker = StringField('Ticker', 
						validators=[DataRequired(), Length(min=2, max=20)])
	submit = SubmitField('Get Ticker')
