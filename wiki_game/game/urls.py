from django.urls import path

from wiki_game.game import views

app_name = "game"
urlpatterns = [
    path("", view=views.GameView.as_view(), name="game"),
    path("start/", view=views.StartGameView.as_view(), name="start"),
    path("finish/", view=views.FinishGameView.as_view(), name="finish"),
    path("leaderboard/", view=views.LeaderboardView.as_view(), name="leaderboard"),
]
