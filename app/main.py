from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from . import models, schemas, crud
from .database import get_db, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JNT CAR Booking API",
    description="API for managing car bookings",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/")
def health_check():
    return {"status": "healthy", "message": "JNT CAR Booking API is running"}

# User endpoints
@app.post("/api/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@app.get("/api/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/api/users/{user_id}/bookings", response_model=List[schemas.BookingResponse])
def read_user_bookings(
    user_id: int, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    # Verify user exists
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.get_bookings(db, skip=skip, limit=limit, user_id=user_id)

# Car endpoints
@app.get("/api/cars/", response_model=List[schemas.CarResponse])
def read_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cars = crud.get_cars(db, skip=skip, limit=limit)
    return cars

@app.get("/api/cars/{car_id}", response_model=schemas.CarResponse)
def read_car(car_id: int, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id=car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car

@app.get("/api/cars/available", response_model=List[schemas.CarResponse])
def get_available_cars(
    pickup_date: datetime,
    drop_date: datetime,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if drop_date <= pickup_date:
        raise HTTPException(
            status_code=400, 
            detail="Drop date must be after pickup date"
        )
    
    cars = crud.get_available_cars(
        db, 
        pickup_date=pickup_date, 
        drop_date=drop_date,
        location=location
    )
    return cars

@app.post("/api/cars/", response_model=schemas.CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    return crud.create_car(db=db, car=car)

# Booking endpoints
@app.post("/api/bookings/", response_model=schemas.BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    # Verify user exists
    db_user = crud.get_user(db, user_id=booking.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify car exists
    db_car = crud.get_car(db, car_id=booking.car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    
    # Check if car is available for the requested dates
    available_cars = crud.get_available_cars(
        db, 
        pickup_date=booking.pickup_date, 
        drop_date=booking.drop_date
    )
    
    if not any(car.id == booking.car_id for car in available_cars):
        raise HTTPException(
            status_code=400, 
            detail="Car is not available for the requested dates"
        )
    
    return crud.create_booking(db=db, booking=booking)

@app.get("/api/bookings/", response_model=List[schemas.BookingResponse])
def read_bookings(
    skip: int = 0, 
    limit: int = 100,
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_bookings(db, skip=skip, limit=limit, user_id=user_id, status=status)

@app.get("/api/bookings/{booking_id}", response_model=schemas.BookingResponse)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@app.put("/api/bookings/{booking_id}", response_model=schemas.BookingResponse)
def update_booking(
    booking_id: int, 
    booking_update: schemas.BookingUpdate,
    db: Session = Depends(get_db)
):
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return crud.update_booking(db, booking_id=booking_id, booking_update=booking_update)

@app.post("/api/bookings/{booking_id}/confirm", response_model=schemas.BookingResponse)
def confirm_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return crud.confirm_booking(db, booking_id=booking_id)

@app.post("/api/bookings/{booking_id}/cancel", response_model=schemas.BookingResponse)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return crud.cancel_booking(db, booking_id=booking_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
