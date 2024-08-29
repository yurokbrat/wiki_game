import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "wiki_game.users"
    verbose_name = _("Users")

    def ready(self) -> None:
        with contextlib.suppress(ImportError):
            import wiki_game.users.signals  # noqa: F401
