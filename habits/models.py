from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название привычки")
    description = models.TextField(blank=True, verbose_name="Описание")
    xp_reward = models.PositiveIntegerField(default=10, verbose_name="XP за выполнение")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    def __str__(self):
        return self.name

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=True)

    class Meta:
        unique_together = ('habit', 'date')

    def __str__(self):
        return f"{self.habit.name} - {self.date}"

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=50, unique=True)

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')