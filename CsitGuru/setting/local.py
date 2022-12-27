import dj_database_url
from CsitGuru.base import *

from .environs import Env

env = Env()
env.read_env()  

DEBUG = True

SITE_ID = 1

SECRET_KEY = env.str("SECRET_KEY")
MIDDLEWARE = [
      "corsheaders.middleware.CorsMiddleware", 
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",


    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:3000",
]



"""
DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql',
        "NAME": 'railway',
        "USER": 'postgres',
        "PASSWORD": 'o2DOClw5d7E1e8yIRqEK',
        "HOST": 'containers-us-west-73.railway.app',
        "PORT": 5640,
    }
}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql',
        "NAME": env.str("DATABASE_NAME"),
        "USER": env.str("DATABASE_USER"),
        "PASSWORD": env.str("DATABASE_PASSWORD"),
        "HOST": env.str("DATABASE_HOST"),
        "PORT": env.str("DATABASE_PORT"),
    }
}


DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql',
        "NAME": 'postgres',
        "USER": 'postgres',
        "PASSWORD": 'ProgrammerGodRobo123',
        "HOST": 'db.cblbmwgycgevasrvfenp.supabase.co',
        "PORT": 5432,
    }
}


"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}



db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES["default"].update(db_from_env)


STATIC_URL = "/staticfiles/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_ROOT = os.path.join(BASE_DIR, "staticfiles/mediafiles")
MEDIA_URL = "/mediafiles/"

# DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


# SMTP CONFIGURATION
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587

EMAIL_HOST_USER = env.str("Email_Host_User")
EMAIL_HOST_PASSWORD = env.str("Email_Host_Password")
