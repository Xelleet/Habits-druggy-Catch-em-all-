from django.urls import path
from . import views

app_name = 'habits'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('habit/create/', views.CreateHabitView.as_view(), name='create_habit'),
    path('habit/<int:id>/complete/', views.CompleteHabitView.as_view(), name='complete_habit'),
    path('habit/<int:id>/delete/', views.DeleteHabitView.as_view(), name='delete_habit'),
]