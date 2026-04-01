from pathlib import Path
import os
import ssl

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ea7mg)&p%-9w#gl7dls2+-3@p&beegt^w-pdd0g^e)o2#lyg%t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allowed hosts for Render and Local Development
ALLOWED_HOSTS = [
    'clearview-webpage.onrender.com', 
    'clearview-fr6i.onrender.com', 
    '.onrender.com', 
    'localhost', 
    '127.0.0.1'
]

# Wildcards for Cloudflare/Tunneling
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://*.trycloudflare.com',
    'https://*.loca.lt', 
]

# Application definition
INSTALLED_APPS = [
    'tasks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Essential for Render styles
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project2.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Australia/Sydney'
USE_I18N = True
USE_TZ = True

# --- STATIC FILES FIXES (Glassmorphism & Backgrounds) ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
# This is the line you were missing to fix the "poor" appearance on Render:
STATIC_ROOT = BASE_DIR / "staticfiles" 

# Optimizes CSS/JS delivery on Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- AUTHENTICATION SETTINGS ---
LOGIN_URL = 'tasks:login'
LOGIN_REDIRECT_URL = 'tasks:index'
LOGOUT_REDIRECT_URL = 'tasks:welcome'

# --- EMAIL SETTINGS (GMAIL) ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'guptamridul2009@gmail.com' 
EMAIL_HOST_PASSWORD = 'fxgfyacjgwufrvla' 
DEFAULT_FROM_EMAIL = 'ZenStack Team <guptamridul2009@gmail.com>'

# Fix for SSL certificate issues on macOS/Local
EMAIL_SSL_CONTEXT = ssl._create_unverified_context()
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WHITENOISE_MIMETYPES = {'.css': 'text/css'}