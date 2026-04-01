"""
Script to seed the database with initial data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, User, Car
from app import crud, schemas
import json

def create_sample_data():
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create sample users
        users_data = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "+919876543210",
                "license_number": "DL-01-2023-0012345",
                "address": "123 Main St, Delhi, India"
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "phone": "+919876543211",
                "license_number": "DL-02-2023-0012346",
                "address": "456 Park Ave, Mumbai, India"
            },
            {
                "first_name": "Mike",
                "last_name": "Johnson",
                "email": "mike.johnson@example.com",
                "phone": "+919876543212",
                "license_number": "DL-03-2023-0012347",
                "address": "789 Market St, Bangalore, India"
            }
        ]
        
        for user_data in users_data:
            # Check if user already exists
            existing_user = crud.get_user_by_email(db, email=user_data["email"])
            if not existing_user:
                user = schemas.UserCreate(**user_data)
                crud.create_user(db=db, user=user)
                print(f"Created user: {user_data['email']}")
        
        # Create sample cars
        cars_data = [
            {
                "name": "Honda City",
                "brand": "Honda",
                "category": "Sedan",
                "transmission": "Manual",
                "fuel": "Petrol",
                "seats": 5,
                "price_per_day": 1500,
                "price_per_hour": 100,
                "image": "https://images.unsplash.com/photo-1550355241-4c4ca8f0f7dd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBjYXIlMjBkcml2aW5nJTIwcm9hZHxlbnwxfHx8fDE3NzQ3MTAzOTZ8MA&ixlib=rb-4.1.0&q=80&w=1080",
                "rating": 45,
                "reviews": 128,
                "features": ["Air Conditioning", "Power Steering", "ABS", "Airbags"],
                "available": True,
                "location": "Delhi"
            },
            {
                "name": "Maruti Swift",
                "brand": "Maruti Suzuki",
                "category": "Hatchback",
                "transmission": "Manual",
                "fuel": "Petrol",
                "seats": 5,
                "price_per_day": 1200,
                "price_per_hour": 80,
                "image": "https://images.unsplash.com/photo-1494976384436-d6f0bfe5c9c5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBjYXIlMjBkcml2aW5nJTIwcm9hZHxlbnwxfHx8fDE3NzQ3MTAzOTZ8MA&ixlib=rb-4.1.0&q=80&w=1080",
                "rating": 43,
                "reviews": 96,
                "features": ["Air Conditioning", "Power Steering", "Central Locking"],
                "available": True,
                "location": "Delhi"
            },
            {
                "name": "Toyota Innova",
                "brand": "Toyota",
                "category": "SUV",
                "transmission": "Manual",
                "fuel": "Diesel",
                "seats": 7,
                "price_per_day": 2500,
                "price_per_hour": 150,
                "image": "https://images.unsplash.com/photo-1542362567-b07e5e58a68a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBjYXIlMjBkcml2aW5nJTIwcm9hZHxlbnwxfHx8fDE3NzQ3MTAzOTZ8MA&ixlib=rb-4.1.0&q=80&w=1080",
                "rating": 47,
                "reviews": 203,
                "features": ["Air Conditioning", "Power Steering", "ABS", "Airbags", "GPS"],
                "available": True,
                "location": "Delhi"
            },
            {
                "name": "Hyundai Creta",
                "brand": "Hyundai",
                "category": "SUV",
                "transmission": "Automatic",
                "fuel": "Diesel",
                "seats": 5,
                "price_per_day": 2000,
                "price_per_hour": 120,
                "image": "https://images.unsplash.com/photo-15493983462-1a9e1cd98276?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBjYXIlMjBkcml2aW5nJTIwcm9hZHxlbnwxfHx8fDE3NzQ3MTAzOTZ8MA&ixlib=rb-4.1.0&q=80&w=1080",
                "rating": 46,
                "reviews": 156,
                "features": ["Air Conditioning", "Power Steering", "ABS", "Airbags", "Touchscreen"],
                "available": True,
                "location": "Mumbai"
            },
            {
                "name": "Tata Nexon",
                "brand": "Tata",
                "category": "SUV",
                "transmission": "Manual",
                "fuel": "Electric",
                "seats": 5,
                "price_per_day": 1800,
                "price_per_hour": 110,
                "image": "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBjYXIlMjBkcml2aW5nJTIwcm9hZHxlbnwxfHx8fDE3NzQ3MTAzOTZ8MA&ixlib=rb-4.1.0&q=80&w=1080",
                "rating": 44,
                "reviews": 89,
                "features": ["Air Conditioning", "Power Steering", "ABS", "Airbags", "Regenerative Braking"],
                "available": True,
                "location": "Mumbai"
            },
            {
                "name": "Mahindra Thar",
                "brand": "Mahindra",
                "category": "SUV",
                "transmission": "Manual",
                "fuel": "Diesel",
                "seats": 4,
                "price_per_day": 2200,
                "price_per_hour": 130,
                "image": "https://images.unsplash.com/photo-1606664515524-ed12e874c98d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBjYXIlMjBkcml2aW5nJTIwcm9hZHxlbnwxfHx8fDE3NzQ3MTAzOTZ8MA&ixlib=rb-4.1.0&q=80&w=1080",
                "rating": 48,
                "reviews": 267,
                "features": ["Air Conditioning", "Power Steering", "4WD", "ABS", "Airbags"],
                "available": True,
                "location": "Bangalore"
            }
        ]
        
        for car_data in cars_data:
            # Check if car already exists
            existing_cars = crud.get_cars(db, skip=0, limit=1000)
            if not any(car.name == car_data["name"] for car in existing_cars):
                car = schemas.CarCreate(**car_data)
                crud.create_car(db=db, car=car)
                print(f"Created car: {car_data['name']}")
        
        print("\n✅ Sample data created successfully!")
        print(f"Created {len(users_data)} users and {len(cars_data)} cars")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
