from django.urls import path,include
from app.views import *
from . import views
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostsView)
router.register(r'likes', LikesView)
router.register(r'comment', CommentsView)
router.register(r'follow', FollowersView)

urlpatterns = [
    path('', include(router.urls)),
    path('authenticate/',jwt_views.TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('create_user/', views.CreateUser.as_view(),name='create_user'),
    path('user/', views.ProfileView.as_view(),name='view_user'),
]