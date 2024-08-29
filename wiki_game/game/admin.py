from django.contrib import admin
from unfold.admin import ModelAdmin

from wiki_game.game.models import GameResult


@admin.register(GameResult)
class CustomAdminClass(ModelAdmin):
    pass
