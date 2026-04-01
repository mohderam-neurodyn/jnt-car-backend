from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from .models import BookingStatus

# User schemas
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    license_number: str
    address: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Car schemas
class CarBase(BaseModel):
    name: str
    brand: str
    category: str
    transmission: str
    fuel: str
    seats: int
    price_per_day: int
    price_per_hour: int
    image: str
    rating: int
    reviews: int
    features: List[str]
    available: bool
    location: str

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Booking schemas
class BookingBase(BaseModel):
    pickup_location: str
    drop_location: str
    pickup_date: datetime
    drop_date: datetime
    payment_method: str

class BookingCreate(BookingBase):
    user_id: int
    car_id: int

class BookingUpdate(BaseModel):
    status: Optional[BookingStatus] = None
    payment_status: Optional[str] = None

class BookingResponse(BookingBase):
    id: int
    user_id: int
    car_id: int
    total_amount: int
    status: BookingStatus
    payment_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional[UserResponse] = None
    car: Optional[CarResponse] = None
    
    class Config:
        from_attributes = True

# Additional schemas for API responses
class BookingListResponse(BaseModel):
    bookings: List[BookingResponse]
    total: int
    page: int
    size: int

class UserWithBookings(UserResponse):
    bookings: List[BookingResponse] = []
