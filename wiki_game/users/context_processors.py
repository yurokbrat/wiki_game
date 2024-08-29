from django.conf import settings
from requests import Request


def allauth_settings(request: Request) -> dict:
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }
