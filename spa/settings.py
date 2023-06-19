import os
import string
from pathlib import Path
from random import choices

from dotenv import load_dotenv
from django.contrib.messages import constants as messages


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str(os.getenv("SECRET_KEY"))

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # Django apps
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "captcha",
    # My apps
    "comments.apps.CommentsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "spa.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "spa.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "PORT": int(os.getenv("DB_PORT")),
        "HOST": str(os.getenv("DB_HOST")),
        "NAME": str(os.getenv("DB_NAME")),
        "USER": str(os.getenv("DB_USER")),
        "PASSWORD": str(os.getenv("DB_PASSWORD")),
    }
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Kiev"

USE_I18N = False

USE_TZ = True

STATIC_URL = "static/"
STATIC_DIR = BASE_DIR / "static"
STATICFILES_DIRS = [STATIC_DIR]
# STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

MESSAGE_TAGS = {messages.INFO: "primary", messages.ERROR: "danger"}


def get_generated_captcha_challenge() -> tuple[str, str]:
    """Returns a generated captcha challenge tuple(challenge, response)."""
    challenge = "".join(choices(string.ascii_uppercase + string.digits, k=5))
    response = challenge.lower()
    return (challenge, response)


CAPTCHA_FONT_SIZE = 35
CAPTCHA_CHALLENGE_FUNCT = get_generated_captcha_challenge
