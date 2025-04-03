# AscendStats

AscendStats is a Django-based web application designed to provide insightful climbing analytics and statistics. It features user authentication, modular app structure, and static file management, making it scalable and easy to deploy.

## Features

- **User Authentication**: Login using email or username with Django Allauth.
- **Custom User Model**: Extendable user model for future enhancements.
- **Static File Management**: Handled with WhiteNoise for production readiness.
- **Responsive Design**: Built with Bootstrap 5 for mobile-friendly layouts.
- **Email Notifications**: Configurable email backend for user notifications.

## Project Structure
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

## Prerequisites

- Python 3.12+
- Django 5.1+
- Docker and Docker Compose (optional for containerized deployment)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AscendStats.git
cd AscendStats
```
