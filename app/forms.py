from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class BusForm(FlaskForm):
    number_of_buses = IntegerField('Number of Buses', validators=[DataRequired()])
    seats_per_bus = IntegerField('Seats per Bus', validators=[DataRequired()])
    submit = SubmitField('Create Buses')

class BookingForm(FlaskForm):
    user_name = StringField('Your Name', validators=[DataRequired()])
    additional_info = StringField('Additional Info', validators=[DataRequired()])
    submit = SubmitField('Confirm Booking')
