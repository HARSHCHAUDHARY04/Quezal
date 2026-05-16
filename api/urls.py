from django.urls import path
from . import views

urlpatterns = [
    path('api/signup', views.api_signup, name='api_signup'),
    path('api/login', views.api_login, name='api_login'),
    path('api/logout', views.api_logout, name='api_logout'),
    path('api/me', views.api_me, name='api_me'),
    path('upload', views.deploy_battle, name='deploy_battle'),
    path('download/<str:filename>', views.download_battle_results, name='download_battle_results'),
    path('api/my-quizzes', views.api_my_quizzes, name='api_my_quizzes'),
    path('api/my-quizzes/<int:quiz_id>', views.api_delete_my_quiz, name='api_delete_my_quiz'),
    path('api/profile', views.api_profile, name='api_profile'),
    path('api/change-password', views.api_change_password, name='api_change_password'),
    path('api/battle-stats', views.get_battle_statistics, name='get_battle_statistics'),
    path('api/take-quiz/<int:quiz_id>', views.api_take_quiz, name='api_take_quiz'),
    path('api/battle-health', views.battle_system_health, name='battle_system_health'),
    path('', views.battle_arena, name='battle_arena'),
    path('user', views.user_dashboard_page, name='user_dashboard_page'),
]
