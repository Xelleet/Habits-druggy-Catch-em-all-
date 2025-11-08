from django.contrib import admin
from .models import Habit, HabitLog, Badge

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display =  ('name', 'user', 'xp_reward')

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'completed')
    list_filter = ('date', 'completed')

@admin.register(Badge)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','code')
    list_filter = ('name', 'code')