from doctest import FAIL_FAST

from CsitGuru.base import *

from .environs import Env

env = Env()
env.read_env() 

DEBUG = True
SECRET_KEY = env.str("SECRET_KEY")
SITE_ID = 2

ALLOWED_HOSTS = ["csitguru.herokuapp.com","csitguru.com", "www.csitguru.com", "csitguru.up.railway.app"]
MIDDLEWARE = [
      "corsheaders.middleware.CorsMiddleware", 
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",  
]

SESSION_COOKIE_AGE = 60 * 60 * 60 * 24

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CORS_ALLOWED_ORIGINS = [
    "https://csitguru.com/",
    "https://www.csitguru.com/",
    "https://csitguru.netlify.app/",

]
CSRF_TRUSTED_ORIGINS = [
    'https://csitguru.up.railway.app'
]




# CACHE FRAMEWORK
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 60  # 1 week
CACHE_MIDDLEWARE_KEY_PREFIX = ""

# HTTP Strict Transport Security
SECURE_HSTS_SECONDS = 15780000  # 6 Months as Recommended
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# X-XSS-Protection
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# CSRF
CSRF_COOKIE_SECURE = True 
SESSION_COOKIE_SECURE = True 

# REDIRECT HTTP TO HTTPS
# SECURE_SSL_REDIRECT = True


import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES["default"].update(db_from_env)


STATIC_URL = "/staticfiles/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
"""
In production, all of your static files must exist in a directory
i.e. STATIC_ROOT and your web server should serve them to the public i.e. STATIC_URL.
"""
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_ROOT = os.path.join(BASE_DIR, "staticfiles/mediafiles")
MEDIA_URL = "/mediafiles/"

# SMTP CONFIGURATION
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587

EMAIL_HOST_USER = env.str("Email_Host_User")
EMAIL_HOST_PASSWORD = env.str("Email_Host_Password")
