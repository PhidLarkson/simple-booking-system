from datetime import datetime, timedelta
from app import db

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seats = db.relationship('Seat', backref='bus', lazy=True)

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='free')  # free, booked, paid
    booked_time = db.Column(db.DateTime, nullable=True)
    user_name = db.Column(db.String(100), nullable=True)
    additional_info = db.Column(db.String(255), nullable=True)

    def is_expired(self):
        if self.status == 'booked' and self.booked_time:
            return datetime.utcnow() > self.booked_time + timedelta(minutes=5)
        return False
