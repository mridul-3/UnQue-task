College Appointment System

This is a Django-based backend system for a College Appointment System that allows students to book appointments with professors. Professors can specify their availability, manage bookings, and students can authenticate, view available slots, and make or cancel appointments.

## Prerequisites

- Python 3.8+
- PostgreSQL
- Chrome Browser (for E2E tests)

## Setup Instructions

1. Clone the repository:

```bash
git clone <repository-url>
cd Shambhu
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the `/appointment_system` directory with the following variables:

```
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

5. Create PostgreSQL database:

```bash
createdb your_db_name
```

6. Run migrations:

```bash
python manage.py makemigrations users
python manage.py makemigrations appointments
python manage.py migrate
```

7. Run the development server:

```bash
python manage.py runserver
```

## Project Structure

- `users/`: Custom user management app
- `appointments/`: Main app handling availability and appointments
- `appointment_system/`: Project settings and configuration

## API Endpoints

### Authentication

- `POST /api/users/login/`: Login and get authentication token
- `POST /api/users/register/`: Register new user

### Appointments

- `GET /api/appointments/`: List appointments
- `POST /api/appointments/`: Create appointment
- `POST /api/appointments/{id}/cancel/`: Cancel appointment

### Availability

- `GET /api/availability/`: List available slots
- `POST /api/availability/`: Create availability (professors only)

## Testing

1. Run E2E tests:

```bash
python manage.py test appointments.e2e_tests
```

Features 1. User Management:
• Professors and Students can register and log in.
• Role-based access control (Professors vs. Students). 2. Appointment Management:
• Professors can add their availability for specific time slots.
• Students can view available time slots and book appointments.
• Professors can cancel appointments.
• Students can view their scheduled appointments. 3. API Endpoints:
• Fully functional REST APIs for user authentication, availability, and appointment management. 4. End-to-End Automated Test Case:
• Tests the entire user flow for booking and managing appointments.

Technology Stack
• Backend Framework: Django (with Django REST Framework)
• Database: PostgreSQL (can be replaced with SQLite for testing purposes)
• Authentication: Token-based authentication using Django REST Framework
• Testing: pytest for automated testing
