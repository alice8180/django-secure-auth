# Django Secure Auth – Backend (Django REST Framework)

A **production-ready secure authentication backend** built with Django REST Framework.  
Supports cookie-based JWT authentication, CSRF protection, email verification, password reset, brute-force protection, and background task handling.

---

## Features

- User Registration & Email Verification (One-Time URL)
- Login & Logout with Cookie-based JWT Authentication
- CSRF Protection for state-changing requests
- Resend Verification Email
- Forgot Password & Reset via One-Time URL
- Brute-force Protection with `django-ratelimit` + Redis
- Background tasks with Celery + RabbitMQ
- Structured **class-based views** & reusable utilities

---

## Requirements

- Python 3.10+
- PostgreSQL (primary database)
- Redis (for brute-force/IP blocking only)
- RabbitMQ (Celery broker for background tasks)
- `uv` (Python package/dependency manager)

---

## Project Structure
django-secure-auth/
├── accounts/ # User models, serializers, views, authentication
│ ├── authentication.py
│ ├── csrf_authentication.py
│ ├── serializers.py
│ ├── views.py
│ ├── signals.py
│ └── ...
│
├── celery_tasks/ # Celery async tasks
│ └── notifications.py
│
├── config/ # Configurations (DB, JWT, Redis, DRF, Celery, Logging)
│ ├── celery_config.py
│ ├── jwt_config.py
│ ├── redis_config.py
│ ├── drf_settings.py
│ ├── logging.py
│ └── spectacular_settings.py
│
├── django_secure_auth/ # Core Django project
│ ├── settings.py
│ ├── urls.py
│ ├── celery.py
│ ├── asgi.py / wsgi.py
│ └── ...
│
├── notifications/ # Notification models & services
│ ├── models.py
│ └── services.py
│
├── utils/ # Common utilities
│ ├── constants.py
│ ├── generate.py
│ ├── generic_api_view.py
│ ├── logger.py
│ └── otp.py
│
├── templates/ # HTML templates (emails)
├── static/ # Static files
├── logs/ # Log files
├── pyproject.toml # uv project file
├── uv.lock # uv dependency lock file
├── main.py # Entry script (if any custom startup logic)
├── manage.py # Django management script
└── README.md # Project documentation



---

## Installation & Setup (with uv)

1. **Clone the repository**
```bash & powershell
git clone https://github.com/your-username/django-secure-auth.git
cd django-secure-auth


2. Create and sync virtual environment with uv:
    uv venv
    source .venv/bin/activate
    uv sync


3. Setup environment variables (.env):
    DEBUG=True
    SECRET_KEY=your-secret-key
    DATABASE_URL=postgres://user:password@localhost:5432/django_secure_auth
    CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
    REDIS_URL=redis://localhost:6379/0


4. Apply migrations:
    uv run python manage.py migrate


5. Run development server:
    uv run python manage.py runserver


6. Run Celery worker:
    uv run celery -A django_secure_auth worker -l info


7. Run Celery beat (if using scheduled tasks):
    uv run celery -A django_secure_auth beat -l info


API Documentation
    Swagger UI → /api/schema/swagger-ui/
    ReDoc → /api/schema/redoc/