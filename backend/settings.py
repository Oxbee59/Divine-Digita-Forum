"""
Django settings for backend project.
Configured for Render deployment with external PostgreSQL database and Cloudinary for media.
"""

import os
import dj_database_url
from pathlib import Path
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------
# SECURITY
# ----------------------------------------------------
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')  # fallback for local
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',') if os.environ.get('ALLOWED_HOSTS') else ["*"]

# ----------------------------------------------------
# INSTALLED APPS
# ----------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'forum',  # your app
    "cloudinary",
    "cloudinary_storage",
]

# ----------------------------------------------------
# MIDDLEWARE
# ----------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

# ----------------------------------------------------
# TEMPLATES
# ----------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'forum' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# ----------------------------------------------------
# DATABASE
# ----------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=os.environ.get('DATABASE_SSL', 'False') == 'True'
    )
}

# ----------------------------------------------------
# PASSWORD VALIDATION
# ----------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------------------------------------
# INTERNATIONALIZATION
# ----------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------
# STATIC FILES
# ----------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'forum' / 'static'
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ----------------------------------------------------
# CLOUDINARY MEDIA FILES
# ----------------------------------------------------
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME", "your_cloud_name"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY", "your_api_key"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET", "your_api_secret"),
}

# Remove local media settings (optional)
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# ----------------------------------------------------
# MESSAGES
# ----------------------------------------------------
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ----------------------------------------------------
# AUTH
# ----------------------------------------------------
LOGIN_URL = '/login/'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
