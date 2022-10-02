from django.urls import path
from app.views import *
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('user/', views.UserCreate.as_view()),
    path('profile/', views.Profileview.as_view()),
    path('token/',
        jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
]