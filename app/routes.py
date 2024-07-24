from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.forms import BusForm, BookingForm
from app.models import Bus, Seat
import weasyprint
from datetime import datetime

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = BusForm()
    if form.validate_on_submit():
        number_of_buses = form.number_of_buses.data
        seats_per_bus = form.seats_per_bus.data
        for _ in range(number_of_buses):
            bus = Bus()
            db.session.add(bus)
            db.session.commit()
            for _ in range(seats_per_bus):
                seat = Seat(bus_id=bus.id)
                db.session.add(seat)
        db.session.commit()
        flash('Buses created successfully', 'success')
        return redirect(url_for('admin'))
    return render_template('admin.html', form=form)

@app.route('/buses')
def buses():
    buses = Bus.query.all()
    for bus in buses:
        for seat in bus.seats:
            if seat.is_expired():
                seat.status = 'free'
                seat.booked_time = None
                seat.user_name = None
                seat.additional_info = None
    db.session.commit()
    return render_template('buses.html', buses=buses)

@app.route('/book/<int:seat_id>')
def book(seat_id):
    seat = Seat.query.get_or_404(seat_id)
    if seat.status == 'free':
        seat.status = 'booked'
        seat.booked_time = datetime.utcnow()
        db.session.commit()
        flash('Seat booked successfully', 'success')
    else:
        flash('Seat is not available', 'danger')
    return redirect(url_for('buses'))

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    selected_seats = request.form.get('selected_seats')
    user_name = request.form.get('user_name')
    additional_info = request.form.get('additional_info')
    
    if not selected_seats:
        flash('No seats selected. Please select seats to book.', 'danger')
        return redirect(url_for('buses'))
    
    try:
        seat_ids = [int(seat_id) for seat_id in selected_seats.split(',') if seat_id]
    except ValueError:
        flash('Invalid seat selection.', 'danger')
        return redirect(url_for('buses'))
    
    seats = Seat.query.filter(Seat.id.in_(seat_ids)).all()
    for seat in seats:
        if seat.is_expired():
            seat.status = 'free'
            seat.booked_time = None
            seat.user_name = None
            seat.additional_info = None
        seat.user_name = user_name
        seat.additional_info = additional_info
    db.session.commit()
    
    return render_template('confirm_booking.html', seats=seats, user=user_name)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    seat_ids = request.form.get('seat_ids')
    seat_ids = [int(seat_id) for seat_id in seat_ids.split(',')]

    # user_name = request.form.get('user_name')
    
    seats = Seat.query.filter(Seat.id.in_(seat_ids)).all()
    for seat in seats:
        seat.status = 'paid'
    db.session.commit()
    
    # Generate PDF receipt
    receipt_html = render_template('receipt_template.html', seats=seats)
    pdf = weasyprint.HTML(string=receipt_html).write_pdf()
    
    with open('app/static/receipt.pdf', 'wb') as f:
        f.write(pdf)
    
    return redirect(url_for('download_receipt'))

@app.route('/download_receipt')
def download_receipt():
    return render_template('receipt.html')
