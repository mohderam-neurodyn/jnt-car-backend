from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from . import models, schemas

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Car CRUD operations
def get_cars(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Car).offset(skip).limit(limit).all()

def get_car(db: Session, car_id: int):
    return db.query(models.Car).filter(models.Car.id == car_id).first()

def get_available_cars(
    db: Session, 
    pickup_date: datetime, 
    drop_date: datetime,
    location: str = None
):
    # Get cars that are not booked during the requested dates
    query = db.query(models.Car).filter(models.Car.available == True)
    
    if location:
        query = query.filter(models.Car.location == location)
    
    # Exclude cars that are already booked during the requested dates
    booked_cars = db.query(models.Car.id).join(models.Booking).filter(
        and_(
            models.Booking.status.in_(['confirmed', 'pending']),
            or_(
                and_(
                    models.Booking.pickup_date <= pickup_date,
                    models.Booking.drop_date >= pickup_date
                ),
                and_(
                    models.Booking.pickup_date <= drop_date,
                    models.Booking.drop_date >= drop_date
                ),
                and_(
                    models.Booking.pickup_date >= pickup_date,
                    models.Booking.drop_date <= drop_date
                )
            )
        )
    )
    
    query = query.filter(~models.Car.id.in_(booked_cars))
    
    return query.all()

def create_car(db: Session, car: schemas.CarCreate):
    # Convert features list to JSON string
    car_data = car.dict()
    car_data['features'] = str(car_data['features'])
    car_data['available'] = str(car_data['available']).lower()
    
    db_car = models.Car(**car_data)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

# Booking CRUD operations
def get_bookings(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    user_id: int = None,
    status: str = None
):
    query = db.query(models.Booking)
    
    if user_id:
        query = query.filter(models.Booking.user_id == user_id)
    
    if status:
        query = query.filter(models.Booking.status == status)
    
    return query.offset(skip).limit(limit).all()

def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def create_booking(db: Session, booking: schemas.BookingCreate):
    # Calculate total amount based on car price and booking duration
    car = get_car(db, booking.car_id)
    if not car:
        raise ValueError("Car not found")
    
    # Calculate days and hours
    duration = booking.drop_date - booking.pickup_date
    days = duration.days
    hours = duration.seconds // 3600
    
    # Calculate total amount
    total_amount = (days * car.price_per_day) + (hours * car.price_per_hour)
    
    # Create booking
    booking_data = booking.dict()
    booking_data['total_amount'] = total_amount
    booking_data['status'] = models.BookingStatus.PENDING
    booking_data['payment_status'] = 'pending'
    
    db_booking = models.Booking(**booking_data)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_booking(db: Session, booking_id: int, booking_update: schemas.BookingUpdate):
    db_booking = get_booking(db, booking_id)
    if db_booking:
        update_data = booking_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_booking, field, value)
        
        db.commit()
        db.refresh(db_booking)
    return db_booking

def cancel_booking(db: Session, booking_id: int):
    return update_booking(db, booking_id, schemas.BookingUpdate(status=models.BookingStatus.CANCELLED))

def confirm_booking(db: Session, booking_id: int):
    return update_booking(db, booking_id, schemas.BookingUpdate(
        status=models.BookingStatus.CONFIRMED,
        payment_status='paid'
    ))
