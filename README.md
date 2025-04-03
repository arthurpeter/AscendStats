# AscendStats

AscendStats is a Django-based web application designed to provide insightful climbing analytics and statistics. It features user authentication, modular app structure, and static file management, making it scalable and easy to deploy.

## Features

- **User Authentication**: Login using email or username with Django Allauth.
- **Custom User Model**: Extendable user model for future enhancements.
- **Static File Management**: Handled with WhiteNoise for production readiness.
- **Responsive Design**: Built with Bootstrap 5 for mobile-friendly layouts.
- **Email Notifications**: Configurable email backend for user notifications.

## Project Structure
```
AscendStats/
├── ascendstats/             # Core project files
│   ├── settings.py          # Project settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI entry point
│   └── asgi.py              # ASGI entry point
├── main/                    # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── templates/           # HTML templates
│   └── static/              # Static files (CSS, JS, images)
├── register/                # User registration and authentication
│   ├── backends.py          # Custom authentication backends
│   └── forms.py             # Registration and login forms
├── staticfiles/             # Collected static files for production
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
└── .env                     # Environment variables
```
## Prerequisites

- Python 3.12+
- Django 5.1+
- Docker and Docker Compose (optional for containerized deployment)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/arthurpeter/AscendStats.git
cd AscendStats
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a .env file in the root directory and define the following variables:
```.env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=your-database-host
```
You only need SECRET_KEY for the development branch.

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```
Access the application at http://127.0.0.1:8000

## Docker Deployment
### 1. Build the Docker Image

```bash
docker build -t ascendstats .
```

### 2. Run the Container
```bash
docker run -p 8000:8000 ascendstats
```
Access the application at http://127.0.0.1:8000

### 3. Using Docker Compose

Alternatively, you can use Docker Compose for easier setup:
```bash
docker-compose up
```

## Static Files

Static files are managed using WhiteNoise. During production, run the following command to collect static files:
```bash
python manage.py collectstatic
```

## Authentication

The project uses a custom authentication backend (EmailOrUsernameBackend) located in register/backends.py. Users can log in using either their email or username.
