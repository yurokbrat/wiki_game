# Generated by Django 5.0.8 on 2024-08-27 20:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_article', models.CharField(max_length=255, verbose_name='Начальная точка')),
                ('end_article', models.CharField(max_length=255, verbose_name='Финальная точка')),
                ('path', models.TextField(verbose_name='Путь до победы')),
                ('time_taken', models.FloatField(verbose_name='Время для победы', default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False, verbose_name='Завершена')),
                ('user', models.ForeignKey(verbose_name="Игрок", on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'результат игры',
                'verbose_name_plural': 'результаты игр',
            },
        ),
    ]
