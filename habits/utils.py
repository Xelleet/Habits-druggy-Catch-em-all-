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
   import math
   level = int(math.sqrt(total_xp))
   xp_for_next = (level + 1) ** 2
   xp_needed = max(0, xp_for_next - total_xp)
   progress_percent = int((total_xp / xp_for_next) * 100) if xp_for_next > 0 else 100
   return {
       'level': level,
       'xp_for_next': xp_for_next,
       'xp_needed': xp_needed,
       'progress_percent': min(progress_percent, 100),
   }
