from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=False)
    license_number = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    bookings = relationship("Booking", back_populates="user")

class Car(Base):
    __tablename__ = "cars"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    brand = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    transmission = Column(String(20), nullable=False)
    fuel = Column(String(20), nullable=False)
    seats = Column(Integer, nullable=False)
    price_per_day = Column(Integer, nullable=False)
    price_per_hour = Column(Integer, nullable=False)
    image = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=False)
    reviews = Column(Integer, nullable=False)
    features = Column(Text, nullable=False)  # JSON string
    available = Column(String(10), default="true", nullable=False)
    location = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    bookings = relationship("Booking", back_populates="car")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    pickup_location = Column(String(200), nullable=False)
    drop_location = Column(String(200), nullable=False)
    pickup_date = Column(DateTime(timezone=True), nullable=False)
    drop_date = Column(DateTime(timezone=True), nullable=False)
    total_amount = Column(Integer, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING, nullable=False)
    payment_method = Column(String(50), nullable=False)
    payment_status = Column(String(20), default="pending", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    car = relationship("Car", back_populates="bookings")
