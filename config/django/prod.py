import sys

from csp.constants import NONCE, NONE, SELF, UNSAFE_INLINE

from config.django.base import *  # noqa: F403
from config.django.base import DJANGO_ADMIN_PATH, WAGTAIL_ADMIN_PATH
from config.env import env
from config.settings.wagtail_prod import *  # noqa: E402, F403

STORAGES = {
    "default": {
        "BACKEND": "config.settings.django_storage.MediaR2Storage",
    },
    "staticfiles": {
        "BACKEND": "src.base.storage.ManifestStaticFilesStorage",
    },
    "wagtailrenditions": {
        "BACKEND": "config.settings.django_storage.WagtailRenditionStorage",
    },
}


DEBUG = env.bool("DEBUG", default=False)

APPEND_SLASH = True

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

DEFAULT_HSTS_SECONDS = 365 * 24 * 60 * 60  # 1 year
SECURE_HSTS_SECONDS = int(env.int("SECURE_HSTS_SECONDS", DEFAULT_HSTS_SECONDS))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "class": "src.base.logging.DjangoJsonRequestFormatter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": sys.stdout,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env.str("DJANGO_LOG_LEVEL", "INFO"),
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": env.str("DJANGO_LOG_BACKENDS_LEVEL", "DEBUG"),
            "propagate": False,
        },
    },
}


EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"

EMAIL_HOST = env.str("EMAIL_HOST", "")
EMAIL_PORT = env.str("EMAIL_PORT", "")
EMAIL_HOST_USER = env.str("EMAIL_USER", "")
EMAIL_HOST_PASSWORD = env.str("EMAIL_PASSWORD", "")
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = env.str("EMAIL_FROM", "")

CONTENT_SECURITY_POLICY = {
    "EXCLUDE_URL_PREFIXES": ["/" + DJANGO_ADMIN_PATH, "/" + WAGTAIL_ADMIN_PATH],
    "DIRECTIVES": {
        "default-src": [NONE],
        "script-src": [SELF, NONCE],
        "style-src": [SELF, UNSAFE_INLINE],
        "font-src": [SELF],
        "img-src": [
            SELF,
            "data:",
            "https://*.giphy.com",
            "https://*.tenor.com",
            "https://*.imgur.com",
            "https://static.mahmoudashraf.dev",
            "https://www.gravatar.com",
        ],
        "media-src": [
            SELF,
            "https://static.mahmoudashraf.dev",
        ],
        "connect-src": [SELF],
        "manifest-src": [SELF],
        "object-src": [NONE],
        "frame-ancestors": [SELF],
        "frame-src": [
            SELF,
            "https://*.youtube.com",
        ],
        "form-action": [
            SELF,
            "https://github.com",
            "https://accounts.google.com",
        ],
        "base-uri": [SELF],
        "upgrade-insecure-requests": True,
    },
}
