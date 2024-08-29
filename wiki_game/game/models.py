from django.db import models

from wiki_game.users.models import User


class GameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Игрок")
    start_article = models.CharField(max_length=255, verbose_name="Начальная точка")
    end_article = models.CharField(max_length=255, verbose_name="Финальная точка")
    path = models.TextField(verbose_name="Путь до победы")
    time_taken = models.FloatField(verbose_name="Время для победы", default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, verbose_name="Завершена")

    class Meta:
        verbose_name = "результат игры"
        verbose_name_plural = "результаты игр"

    def __str__(self) -> str:
        super().__str__()
        return f"Игра №{self.id} - Игрок №{self.user_id} - {self.time_taken} секунд"
