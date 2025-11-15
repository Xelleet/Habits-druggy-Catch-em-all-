from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .form import HabitForm
from .utils import get_total_xp, calculate_level, get_level_info
from django.utils.decorators import method_decorator
from .models import Habit, HabitLog, Badge, UserBadge, Profile
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count, Sum, F, Q
from .form import RegisterForm, LoginForm
from django.contrib.auth import login


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'auth/register.html', {'form': form})
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('habits:profile')
        return render(request, 'auth/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})
    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request ,user)
            return redirect('habits:profile')
        return render(request, 'auth/login.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        habits_with_stats = Habit.objects.filter(user=request.user).annotate(
            completion_count=Count("habitlog", filter=Q(habitlog__completed=True)),
            total_xp_from_habit=F('xp_reward') * Count('habitlog', filter=Q(habitlog__completed=True))
        ).order_by('-total_xp_from_habit')

        total_xp = get_total_xp(request.user)
        level_info = get_level_info(total_xp)

        total_xp = get_total_xp(request.user) #ToDO: нужно, чтобы мы получали total xp для каждой привычки отдельно
        level = calculate_level(total_xp)
        badges = UserBadge.objects.filter(user=request.user).select_related('badge')
        profile = Profile.objects.get(user=request.user)
        return render(request, 'habits/profile.html', {'profile': profile, 'total_xp': total_xp, 'level': level,
        'badges': badges, 'habits_with_stats':habits_with_stats ,'habits': Habit.objects.filter(user=request.user),
        'xp_for_next_level': level_info['xp_for_next'], 'xp_needed': level_info['xp_needed'], 'progress_percent': level_info['progress_percent'],
        })

@method_decorator(login_required, name='dispatch')
class CreateHabitView(View):
    def get(self, request):
        form = HabitForm()
        return render(request, 'habits/create_habit.html', {'form': form})
    def post(self, request):
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()

            if len(Habit.objects.filter(user=request.user)) >= 1: #На случай, если наше приложение окажется дырявым проверяем значения больше одного (а то мало ли)
                badge = Badge.objects.filter(code='FIRST_HABIT').first()
                if badge:
                    UserBadge.objects.get_or_create(user=request.user, badge=badge)

            return redirect('habits:profile')
        return render(request, 'habits/create_habit.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class CompleteHabitView(View):
    def get(self, request, *args, **kwargs):
        import math
        habit = get_object_or_404(Habit, id=self.kwargs['id'])
        if habit.user == request.user:
            HabitLog.objects.create(habit=habit)

            check_streak(3, habit, request.user)
            check_streak(7, habit, request.user)
            check_habits_count(3, request.user)
            check_100xp(request.user)

            total_xp = get_total_xp(request.user)
            old_level = int(math.sqrt(total_xp - habit.xp_reward))  # уровеньДО
            new_level = int(math.sqrt(total_xp))

            response_data = {
                'success': True,
                'xp_gained': habit.xp_reward,
                'total_xp': total_xp,
                'level_up': new_level > old_level,
                'new_level': new_level,
            }

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(response_data)
        return redirect('habits:profile')

@method_decorator(login_required, name='dispatch')
class DeleteHabitView(View):
    def get(self, request, *args, **kwargs):
        habit = Habit.objects.get(id=self.kwargs['id'])
        if habit.user == request.user:
            habit.delete()
        return redirect('habits:profile')

def check_100xp(user):
    total_xp = get_total_xp(user)
    if total_xp >= 100:
        badge = Badge.objects.filter(code='XP_100').first()
        if badge:
            UserBadge.objects.get_or_create(user=user, badge=badge)

def check_streak(count, habit, user):
    date_list = [timezone.now().date() - timedelta(days=i) for i in range(count)]
    streak = HabitLog.objects.filter(
        habit=habit,
        date__date__in=date_list, #Я хз как именно у нас будут выполняться привычки, но допустим, что раз в день и конкретное время не имеет значение
        completed=True
    ).count()
    if streak > count:
        badge = Badge.objects.filter(code=f'STREAK_{count}').first()
        if badge:
            UserBadge.objects.get_or_create(user=user, badge=badge)

def check_habits_count(count, user):
    habits_count = len(HabitLog.objects.filter(habit__user=user))
    if habits_count >= habits_count:
        badge = Badge.objects.filter(code=f'DIVERSE_{count}').first()
        if badge:
            UserBadge.objects.get_or_create(user=user, badge=badge)