# JNT CAR Booking API

A FastAPI-based booking system for JNT CAR rental service with PostgreSQL database.

## Features

- User management (registration, profile)
- Car management (listing, availability check)
- Booking system (create, update, cancel, confirm bookings)
- Real-time availability checking
- Payment status tracking
- RESTful API with Pydantic schemas
- Database migrations with Alembic

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Powerful relational database
- **SQLAlchemy** - SQL Toolkit and ORM
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip or poetry

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend-booking
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database configuration
```

5. Set up PostgreSQL database:
```sql
CREATE DATABASE jntcar_booking;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE jntcar_booking TO postgres;
```

6. Run database migrations:
```bash
alembic upgrade head
```

7. Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Users
- `POST /api/users/` - Create a new user
- `GET /api/users/{user_id}` - Get user by ID
- `GET /api/users/{user_id}/bookings` - Get user's bookings

### Cars
- `GET /api/cars/` - List all cars
- `GET /api/cars/{car_id}` - Get car by ID
- `GET /api/cars/available` - Get available cars for specific dates
- `POST /api/cars/` - Create a new car (admin)

### Bookings
- `POST /api/bookings/` - Create a new booking
- `GET /api/bookings/` - List all bookings (with filters)
- `GET /api/bookings/{booking_id}` - Get booking by ID
- `PUT /api/bookings/{booking_id}` - Update booking
- `POST /api/bookings/{booking_id}/confirm` - Confirm booking
- `POST /api/bookings/{booking_id}/cancel` - Cancel booking

### Health Check
- `GET /` - Health check endpoint

## Database Schema

### Users Table
- `id` (Primary Key)
- `first_name`, `last_name`
- `email` (Unique)
- `phone`, `license_number`, `address`
- `created_at`, `updated_at`

### Cars Table
- `id` (Primary Key)
- `name`, `brand`, `category`
- `transmission`, `fuel`, `seats`
- `price_per_day`, `price_per_hour`
- `image`, `rating`, `reviews`
- `features` (JSON string)
- `available`, `location`
- `created_at`, `updated_at`

### Bookings Table
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `car_id` (Foreign Key)
- `pickup_location`, `drop_location`
- `pickup_date`, `drop_date`
- `total_amount`
- `status` (pending, confirmed, cancelled, completed)
- `payment_method`, `payment_status`
- `created_at`, `updated_at`

## Usage Examples

### Create a User
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "license_number": "DL123456",
    "address": "123 Main St, City, State"
  }'
```

### Check Available Cars
```bash
curl "http://localhost:8000/api/cars/available?pickup_date=2024-01-15T10:00:00&drop_date=2024-01-17T10:00:00&location=Delhi"
```

### Create a Booking
```bash
curl -X POST "http://localhost:8000/api/bookings/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "car_id": 1,
    "pickup_location": "Delhi Airport",
    "drop_location": "Delhi Airport",
    "pickup_date": "2024-01-15T10:00:00",
    "drop_date": "2024-01-17T10:00:00",
    "payment_method": "card"
  }'
```

## Development

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migrations:
```bash
alembic downgrade -1
```

### Running Tests

```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest
```

## Production Deployment

1. Set environment variables for production
2. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

3. Use environment variables for sensitive data
4. Set up proper database connection pooling
5. Configure CORS for your frontend domain

## License

This project is licensed under the MIT License.
