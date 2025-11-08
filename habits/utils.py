from django.db import models
from .models import HabitLog

def get_total_xp(user):
    total = HabitLog.objects.filter(
        habit__user=user,
        completed=True
    ).aggregate(
        total_xp = models.Sum('habit__xp_reward')
    )['total_xp'] or 0
    return total

def calculate_level(total_xp):
    import math
    return int(math.sqrt(total_xp or 0))