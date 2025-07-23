from django.urls import path
from . import views

app_name = 'maktab'

urlpatterns = [
    path('', views.home, name='home'),
    # Metodikalar URLs
    path('metodikalar/', views.grade_list, name='metodikalar'),  # Alias for metodikalar
    path('methodologies/', views.grade_list, name='grade_list'),  # Sinflar ro'yxati
    path('methodologies/grade/<int:grade_id>/', views.subject_list, name='subject_list'),  # Fanlar ro'yxati
    path('methodologies/subject/<int:subject_id>/', views.section_list, name='section_list'),  # Qismlar ro'yxati
    path('methodologies/section/<int:section_id>/', views.lesson_list, name='lesson_list'),  # Darslar ro'yxati
    path('methodologies/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),  # Dars batafsil
    
    # Darsliklar URLs
    path('textbooks/', views.textbook_list, name='textbook_list'),
    path('textbooks/<int:textbook_id>/lesson/<int:lesson_id>/', views.textbook_detail, name='textbook_detail'),
    
    # Vazifalar URLs
    path('tasks/', views.task_list, name='task_list'),  # Sinflar ro'yxati
    path('tasks/grade/<int:grade_id>/', views.task_subject_list, name='task_subject_list'),  # Fanlar ro'yxati
    path('tasks/section/<int:section_id>/', views.task_by_subject, name='task_by_subject'),  # Vazifalar ro'yxati
    path('tasks/detail/<int:task_id>/', views.task_detail, name='task_detail'),  # Vazifa batafsil
    
    # Authentication URLs
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
]