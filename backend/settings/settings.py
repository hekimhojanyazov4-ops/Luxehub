from datetime import timedelta
import os
from pathlib import Path
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


SECRET_KEY = load_dotenv(".env", "SECRET_KEY")

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",

    # "drf_spectacular_sidecar",
    
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR / 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR/'media')



# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



AUTH_USER_MODEL = 'api.User'

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
     "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),

    "PAGE_SIZE": 12,

    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],

    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    # Token lifetimes
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),

    # Refresh token rotation & blacklisting
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,

    # Signing & claims
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,  # Or a dedicated secret key in production
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    # Authorization header: "Authorization: Bearer <token>"
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",

    # Works seamlessly with UUID primary keys (like your Base model's id)
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",
}


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_HOSTS = [
    "127.0.0.1:5174",
    "localhost:5173"
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'





SPECTACULAR_SETTINGS = {
    # ---------------------------------------------------------
    # API INFORMATION
    # ---------------------------------------------------------

    "TITLE": "LuxeHub Hotel Management API",
    "DESCRIPTION": """
# LuxeHub — Hotel Management Platform

Welcome to the official LuxeHub REST API documentation.

A comprehensive hotel reservation and management platform
built with Django REST Framework.

## Core Features

- JWT authentication and user management
- Hotel room management
- Room images and galleries
- Room availability checking
- Reservation management
- Reservation cancellation
- Reservation status management
- Payment management
- Customer reviews and ratings
- Favourite rooms
- Newsletter subscriptions

## User Roles

- ADMIN: Full platform administration.
- MANAGER: Hotel and reservation management.
- CUSTOMER: Room browsing and personal reservations.

## Authentication

Most protected endpoints require JWT authentication.

1. Register or log in.
2. Obtain your access token.
3. Click Authorize in Swagger UI.
4. Enter your JWT access token.

Enjoy exploring the LuxeHub API!
""",

    "VERSION": "1.0.0",

    "SERVE_INCLUDE_SCHEMA": False,

    # ---------------------------------------------------------
    # API ORGANIZATION
    # ---------------------------------------------------------

    "TAGS": [
        {
            "name": "Authentication",
            "description": "Registration, login and user profiles.",
        },
        {
            "name": "Rooms",
            "description": "Browse, create, update and manage hotel rooms.",
        },
        {
            "name": "Room Images",
            "description": "Manage room images and galleries.",
        },
        {
            "name": "Reservations",
            "description": "Create, view, cancel and manage reservations.",
        },
        {
            "name": "Payments",
            "description": "Payment records and transaction management.",
        },
        {
            "name": "Favourites",
            "description": "Manage your favourite hotel rooms.",
        },
        {
            "name": "Reviews",
            "description": "Customer reviews and room ratings.",
        },
        {
            "name": "Newsletter",
            "description": "Newsletter subscriptions and management.",
        },
    ],

    # ---------------------------------------------------------
    # AUTHENTICATION
    # ---------------------------------------------------------

    "COMPONENTS": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter your JWT access token.",
            },
        },
    },

    "SECURITY": [
        {"BearerAuth": []},
    ],

    # ---------------------------------------------------------
    # SCHEMA GENERATION
    # ---------------------------------------------------------

    "SCHEMA_PATH_PREFIX": r"/api/",

    "SCHEMA_PATH_PREFIX_TRIM": False,

    "SORT_OPERATIONS": True,

    "SORT_OPERATION_PARAMETERS": True,

    "CAMELIZE_NAMES": False,

    "ENUM_GENERATE_CHOICE_DESCRIPTION": True,

    "COMPONENT_SPLIT_REQUEST": True,

    "COMPONENT_NO_READ_ONLY_REQUIRED": True,

    "DISABLE_ERRORS_AND_WARNINGS": False,

    # ---------------------------------------------------------
    # SWAGGER UI
    # ---------------------------------------------------------

    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "displayOperationId": False,
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2,
        "displayRequestDuration": True,
        "filter": True,
        "persistAuthorization": True,
        "docExpansion": "list",
        "tryItOutEnabled": True,
    },

    "REDOC_DIST": "SIDECAR",
    "SWAGGER_UI_DIST": "SIDECAR",

    # ---------------------------------------------------------
    # EXAMPLES
    # ---------------------------------------------------------

    "APPEND_COMPONENTS": {},

    "EXTENSIONS_INFO": {
        "x-logo": {
            "url": "https://example.com/logo.png",
            "altText": "LuxeHub Logo",
        },
    },
}
