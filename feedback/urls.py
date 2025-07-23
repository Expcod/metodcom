from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('create/', views.feedback_create, name='create'),
    path('ajax/', views.feedback_ajax, name='ajax'),
]
