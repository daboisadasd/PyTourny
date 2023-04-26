# Django settings for PyTourny project.

import os
from pathlib import Path

# import the Django secret key from a separate file called "keys.py"
from keys import django_secret

# Define the project base directory by resolving the parent directory twice
BASE_DIR = Path(__file__).resolve().parent.parent

# Set the Django secret key
SECRET_KEY = django_secret

# Enable debug mode for development
DEBUG = True

# Set the allowed hosts for this project
ALLOWED_HOSTS = []

# Configure the installed apps for the project
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "PyTournyApp",
]

# Set the middleware classes for the project
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Set the root URL configuration for the project
ROOT_URLCONF = "PyTourny.urls"

# Set the template engine for the project
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
            ],
        },
    },
]

# Set the WSGI application for the project
WSGI_APPLICATION = "PyTourny.wsgi.application"

# Configure the default database for the project
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Set the password validators for the project
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Set the language code for the project
LANGUAGE_CODE = "en-us"

# Set the time zone for the project. Examples:
# - US Eastern time: 'America/New_York'
# - Europe/London time: 'Europe/London'
# - Asia/Tokyo time: 'Asia/Tokyo'
# - Australia/Sydney time: 'Australia/Sydney'
# - Africa/Johannesburg time: 'Africa/Johannesburg'
# - South America/Sao_Paulo time: 'America/Sao_Paulo'
TIME_ZONE = "America/New_York"

# Use internationalization in the project
USE_I18N = True

# Use localization in the project
USE_L10N = True

# Use time zone support in the project
USE_TZ = True

# Set the URL path for static files in the project
STATIC_URL = "/static/"

# Set the directory path for static files in the project
STATIC_ROOT = os.path.join(BASE_DIR, "static")
