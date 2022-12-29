import logging
import os
import sys
from django.core.exceptions import ImproperlyConfigured



# Helpers
def get_bool_from_environment(name, default=False):
    return os.getenv(name, default) in ["True", "true", True]

def get_list_from_environment(name, default=None):
    return [item.strip() for item in os.environ[name].split(",")] if name in os.environ else default if default else []



# Basic settings
ALLOWED_HOSTS           = get_list_from_environment("ALLOWED_HOSTS")
CSRF_COOKIE_SECURE      = get_bool_from_environment("CSRF_COOKIE_SECURE")
CSRF_TRUSTED_ORIGINS    = get_list_from_environment("CSRF_TRUSTED_ORIGINS")
DEBUG                   = get_bool_from_environment("DEBUG")
DJANGOAPPS_DIRECTORY    = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # One level up from the current directory
DJANGOPROJECT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Two levels up from the current directory
SECRET_KEY              = os.environ.get("SECRET_KEY", "defaulT_k3y")
SESSION_COOKIE_SECURE   = get_bool_from_environment("SESSION_COOKIE_SECURE") # if True then sends session cookies only over HTTPS
WEBSITE_BASE_URL        = os.environ.get("WEBSITE_BASE_URL", "http://localhost")



# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(DJANGOPROJECT_DIRECTORY, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]



# Database
DATABASES = {
    "default": {
        "ENGINE":   os.environ.get("DATABASE_ENGINE", "django.db.backends.postgresql_psycopg2"),
        "HOST":     os.environ.get("DATABASE_HOST"),
        "PORT":     os.environ.get("DATABASE_PORT", "5432"),
        "NAME":     os.environ.get("DATABASE_NAME"),
        "USER":     os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "OPTIONS":  { "sslmode": os.environ.get("DATABASE_SSLMODE") },
    },
}



# Password validation
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



# Log errors to stdout (including errors)
LOGGING = {
   "version": 1,
   "disable_existing_loggers": False,
   "formatters": {
       "verbose": {
           "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
       },
   },
   "handlers": {
       "console": {
           "level": "WARNING",
           "class": "logging.StreamHandler",
           "stream": sys.stdout,
           "formatter": "verbose"
       },
   },
   "loggers": {
       "": {
           "handlers": ["console"],
           "level": "WARNING",
           "propagate": True,
       },
   },
}



# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True



# Sessions
SESSION_EXPIRE_AT_BROWSER_CLOSE = True



# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(DJANGOPROJECT_DIRECTORY, "static")
if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)

STATIC_URL = "/static/"
