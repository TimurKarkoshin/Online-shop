"""
Django site_settings for config project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of site_settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from dotenv import dotenv_values
from setting_constance.setting_constance import *  # noqa

# from constance import config
import dj_database_url
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

config = dotenv_values(os.path.join("..", ".env"))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development site_settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-=e-i4dlx_qq&ra7un4)u8bdr#08q)gc_*yyy4@7--kt(0(p#!("

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "constance",
    "constance.backends.database",
    "profiles",
    "products",
    "shops",
    "comments",
    "sliders",
    "django_jinja",
    "django_extensions",
    "basket",
    "django_celery_results",
    "django_celery_beat",
    "history",
    "order",
]

# email configs
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.yandex.ru"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = config["EMAIL_USER"]
EMAIL_HOST_PASSWORD = config["EMAIL_PASSWORD"]

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "app_dirname": "templates",
            "environment": "jinja2_env.environment",
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
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
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {"default": dj_database_url.parse(config["DATABASE_URL"])}

REDIS_URL = config["REDIS_URL"]

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_REDIS_CONNECTION = {
    "default": {
        "BACKEND": "constance.backends.redisd.RedisBackend",
        "LOCATION": REDIS_URL,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

CONSTANCE_DATABASE_CACHE_BACKEND = "default"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# EMAIl AUTHENTICATION
AUTHENTICATION_BACKENDS = [
    "profiles.backends.EmailBackend",
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/


LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

USE_L10N = True

LOCALE_PATHS = [BASE_DIR / "locale/"]

LANGUAGES = [("en", _("English")), ("ru", _("Russian"))]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = reverse_lazy("profiles:login")

SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True

BASKET_SESSION_ID = "basket"
ORDER_SESSION_ID = "order"

LOGFILE_NAME_ERROR = BASE_DIR / "error_logs.txt"
LOGFILE_NAME = BASE_DIR / "info_log.txt"
LOGFILE_SIZE = 5 * 1024 * 1024
LOGFILE_COUNT = 3

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "error_logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGFILE_NAME_ERROR,
            "maxBytes": LOGFILE_SIZE,
            "backupCount": LOGFILE_COUNT,
            "formatter": "verbose",
            "level": "ERROR",
        },
        "info_logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGFILE_NAME,
            "maxBytes": LOGFILE_SIZE,
            "backupCount": LOGFILE_COUNT,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": [
            "console",
            "error_logfile",
            "info_logfile",
        ],
        "level": "INFO",
    },
}

CELERY_BROKER_URL = REDIS_URL
CELERY_TASK_TRACK_STARTED = True

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_BROKER_TRANSPORT_OPTION = {"visibility_timeout": 3600}
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_TASK_DEFAULT_QUEUE = "default"
