from .base import *

CORS_ALLOW_HEADERS = list(default_headers) + [
    "Access-Control-Allow-Origin",
]
#
DEBUG_PROPAGATE_EXCEPTIONS = False
CORS_ORIGIN_WHITELIST = ["https://wwww.frontend.com"]
ALLOWED_HOSTS = ["https://wwww.frontend.com"]
DEBUG = False
CORS_ORIGIN_ALLOW_ALL = True

if os.name == "nt":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": get_secret("DB_NAME"),
            "USER": get_secret("DB_USERNAME"),
            "PASSWORD": get_secret("DB_PASSWORD"),
            "HOST": get_secret("DB_HOST"),
            "PORT": get_secret("DB_PORT"),
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": get_secret("DB_NAME"),
            "USER": get_secret("DB_USERNAME"),
            "PASSWORD": get_secret("DB_PASSWORD"),
            "HOST": get_secret("DB_HOST"),
            "PORT": get_secret("DB_PORT"),
        },
        "replica": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": get_secret("DB_NAME"),
            "USER": get_secret("DB_USERNAME"),
            "PASSWORD": get_secret("DB_PASSWORD"),
            "HOST": get_secret("DB_REPLICA_HOST"),
            "PORT": get_secret("DB_PORT"),
        },
    }
