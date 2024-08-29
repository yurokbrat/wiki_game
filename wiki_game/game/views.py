import re
from typing import Any

import wikipediaapi
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.html import escape
from django.views.generic import FormView, TemplateView, View

from wiki_game.game.forms import StartGameForm
from wiki_game.game.models import GameResult
from wiki_game.users.models import User
from wiki_game.utils import format_duration

wiki_html = wikipediaapi.Wikipedia(
    user_agent="WikiGame (yurokbrat@yandex.ru)",
    language="ru",
    extract_format=wikipediaapi.ExtractFormat.HTML,
)


class GameView(LoginRequiredMixin, View):
    def get(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        game_id = request.GET.get("game_id")
        article = request.GET.get("article")

        if not game_id or not article:
            return redirect("game:start")
        try:
            game_result = GameResult.objects.get(id=game_id)
        except GameResult.DoesNotExist:
            return redirect("game:start")

        article = article.capitalize()
        end_article = game_result.end_article

        if article == end_article:
            return self.handle_game_completion(game_result, request)

        return self.handle_article_view(game_result, article)

    def handle_game_completion(
        self,
        game_result: GameResult,
        request: ASGIRequest,
    ) -> HttpResponse:
        base_points = 10
        optimal_path_length = 5
        actual_path_length = len(game_result.path.split(" -> "))
        path_bonus = max(0, round((optimal_path_length / actual_path_length) * 5))

        if not game_result.completed:
            duration_seconds = (timezone.now() - game_result.timestamp).total_seconds()
            game_result.time_taken = duration_seconds
            time_bonus = max(0, 5 - round(duration_seconds / 60))
            total_points = base_points + path_bonus + time_bonus
            game_result.user.rating += total_points
            game_result.path += f" -> {game_result.end_article}"
            game_result.completed = True
            game_result.user.save()
            game_result.save()
        else:
            time_bonus = max(0, 5 - round(game_result.time_taken / 60))
            total_points = base_points + path_bonus + time_bonus

        recent_games = GameResult.objects.filter(
            user_id=request.user.id,
            completed=True,
        ).order_by("time_taken")[:5]

        formatted_recent_games = [
            {
                "start_article": game.start_article,
                "end_article": game.end_article,
                "time_taken": format_duration(game.time_taken),
            }
            for game in recent_games
        ]

        return render(
            request,
            "game/results.html",
            {
                "time_taken": format_duration(game_result.time_taken),
                "path": game_result.path,
                "start_article": game_result.start_article,
                "end_article": game_result.end_article,
                "user_rating": game_result.user.rating,
                "rating_obtain": total_points,
                "base_points": base_points,
                "path_bonus": path_bonus,
                "time_bonus": time_bonus,
                "recent_games": formatted_recent_games,
                "actual_path_length": actual_path_length,
            },
        )

    def handle_article_view(
        self,
        game_result: GameResult,
        article: str,
    ) -> HttpResponse:
        page = wiki_html.page(article)
        content = page.text
        links = page.links

        if content == "":
            return render(
                self.request,
                "game/empty_result.html",
                {"end_article": game_result.end_article},
            )

        for article_title in links:
            content = re.sub(
                rf"\b{re.escape(article_title)}\b",
                f"<a href='/game/?article={escape(article_title)}"
                f"&game_id={game_result.id}'>{escape(article_title)}</a>",
                content,
            )

        game_result.path += f" -> {article}"
        game_result.save()

        return render(
            self.request,
            "game/pages.html",
            {
                "page": content,
                "article": article,
                "end_article": game_result.end_article,
                "game_id": game_result.id,
            },
        )


class StartGameView(LoginRequiredMixin, FormView):
    template_name = "game/start_game.html"
    form_class = StartGameForm

    def form_valid(self, form: StartGameForm) -> HttpResponse:
        start_article = form.cleaned_data["start_article"].capitalize()
        end_article = form.cleaned_data["end_article"].capitalize()
        game_result = GameResult.objects.create(
            user=self.request.user,  # type: ignore[misc]
            start_article=start_article,
            end_article=end_article,
            path=start_article,
            time_taken=0,
        )
        return redirect(
            f"/game/?article={escape(start_article)}&game_id={game_result.id}",
        )


class FinishGameView(LoginRequiredMixin, View):
    def post(self, request: ASGIRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if game_id := request.POST.get("game_id"):
            GameResult.objects.filter(id=game_id).delete()
        return redirect("game:start")


class LeaderboardView(TemplateView):
    template_name = "game/leaders.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["leaders"] = User.objects.order_by("-rating")[:10]
        return context
