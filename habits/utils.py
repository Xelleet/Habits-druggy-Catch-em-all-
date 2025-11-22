from django.db import models
from .models import HabitLog
import math

# Настройка: база экспоненциального роста
XP_BASE = 1.8  # Увеличьте, чтобы рост был быстрее (например, 2.0, 2.5)


def get_total_xp(user):
    total = HabitLog.objects.filter(
        habit__user=user,
        completed=True
    ).aggregate(
        total_xp=models.Sum('habit__xp_reward')
    )['total_xp'] or 0
    return total


def calculate_level(total_xp):
    if total_xp <= 0:
        return 0
    return int(math.log(total_xp, XP_BASE))


def get_level_info(total_xp):
    """
    Возвращает словарь:
    {
        'level': int,
        'xp_for_next': int,
        'xp_needed': int,
        'progress_percent': int (0–100)
    }
    """
    if total_xp <= 0:
        return {
            'level': 0,
            'xp_for_next': int(XP_BASE),
            'xp_needed': int(XP_BASE),
            'progress_percent': 0,
        }

    level = int(math.log(total_xp, XP_BASE))
    xp_for_next = int(XP_BASE ** (level + 1))
    xp_needed = max(0, xp_for_next - total_xp)
    progress_percent = int((total_xp / xp_for_next) * 100) if xp_for_next > 0 else 100

    return {
        'level': level,
        'xp_for_next': xp_for_next,
        'xp_needed': xp_needed,
        'progress_percent': min(progress_percent, 100),
    }