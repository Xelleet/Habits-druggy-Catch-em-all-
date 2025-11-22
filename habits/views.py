from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from .form import HabitForm
from .utils import get_total_xp, calculate_level, get_level_info
from django.utils.decorators import method_decorator
from .models import Habit, HabitLog, Badge, UserBadge, Profile, User
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

        Profile.objects.get(user=request.user).total_xp = get_total_xp(request.user) #ToDO: нужно, чтобы мы получали total xp для каждой привычки отдельно
        total_xp = Profile.objects.get(user=request.user).total_xp
        total_active_users = User.objects.filter(habit__habitlog__completed=True).distinct().count()
        user_rank = User.objects.filter(
            profile__total_xp__gt=request.user.profile.total_xp
        ).count() + 1
        level = calculate_level(total_xp) #ToDO: По хорошему надо ещё с помощью AJAX передавать изменения не только бара, но и циферок в целом
        level_info = get_level_info(total_xp)
        badges = UserBadge.objects.filter(user=request.user).select_related('badge')
        profile = Profile.objects.get(user=request.user)
        return render(request, 'habits/profile.html', {'profile': profile, 'total_xp': total_xp, 'level': profile.level,
        'badges': badges, 'habits_with_stats':habits_with_stats ,'habits': Habit.objects.filter(user=request.user),
        'xp_for_next_level': level_info['xp_for_next'], 'xp_needed': level_info['xp_needed'], 'progress_percent': level_info['progress_percent'],
        'user_rank': user_rank, 'total_active_users': total_active_users
        })

@method_decorator(login_required, name='dispatch')
class LeaderboardView(View):
    def get(self, request):
        leaderboard = Profile.objects.filter(total_xp__gt=0).order_by('-total_xp')[:10]
        total_active_users = User.objects.filter(habit__habitlog__completed=True).distinct().count()
        user_rank = Profile.objects.filter(
            total_xp__gt=Profile.objects.get(user=request.user).total_xp
        ).count() + 1
        return render(request, 'habits/leaderboard.html', {'leaderboard': leaderboard, 'profile': Profile.objects.get(user=request.user), 'user_rank': user_rank, 'total_active_users': total_active_users})

class PublicProfileView(View):
    def get(self, request, id):
        profile = get_object_or_404(Profile, id=id)
        user_badges = UserBadge.objects.filter(user=profile.user).select_related('badge').order_by('-awarded_at').values("badge__name", 'awarded_at')[:3]
        user_rank = Profile.objects.filter(total_xp__gt=profile.total_xp).count()+1
        return render(request, 'habits/public_profile.html', {'profile': profile, 'user_badges': user_badges, 'user_rank': user_rank})

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

            profile = Profile.objects.get(user=request.user)
            profile.total_xp = get_total_xp(request.user)

            # Рассчитываем уровень и прогресс с помощью новой функции
            level_info = get_level_info(profile.total_xp)

            # Уровень ДО — нужно пересчитать от (total_xp - habit.xp_reward)
            old_level_info = get_level_info(profile.total_xp - habit.xp_reward)
            old_level = old_level_info['level']
            new_level = level_info['level']

            # Обновляем уровень в профиле
            profile.level = new_level
            profile.save()

            response_data = {
                'success': True,
                'xp_gained': habit.xp_reward,
                'total_xp': profile.total_xp,
                'xp_for_next_level': level_info['xp_for_next'],
                'xp_needed': level_info['xp_needed'],
                'level_up': new_level > old_level,
                'level': new_level,
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