from django.urls import path
from app.views import *
from . import views

urlpatterns = [
    path('user/', views.UserCreate.as_view()),
    path('profile/', views.Profileview.as_view())
]