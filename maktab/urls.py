from django.urls import path
from . import views

app_name = 'maktab'

urlpatterns = [
    path('', views.home, name='home'),
    path('methodologies/', views.grade_list, name='grade_list'),
    path('methodologies/grade/<int:grade_id>/', views.subject_list, name='subject_list'),
    path('methodologies/subject/<int:subject_id>/', views.section_list, name='section_list'),
    path('methodologies/section/<int:section_id>/', views.lesson_list, name='lesson_list'),
    path('methodologies/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('textbooks/', views.textbook_list, name='textbook_list'),
    path('textbooks/<int:textbook_id>/lesson/<int:lesson_id>/', views.textbook_detail, name='textbook_detail'),
]