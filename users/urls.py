from django.urls import path

from .views import (
    register, login, logout, AuthenticatedUser, PermissionAPIView, RoleViewSet,
     UserGenericAPIView,
    ProfileInfoAPIView, ProfilePasswordAPIView,listroleview,UserAPIView,
    RoleViewSet,UserlistAPI
)

urlpatterns = [
    path('register', register),
    path('login', login),
    path('logout', logout),

    path('user', AuthenticatedUser.as_view()),
    path('users/<int:pk>', UserAPIView.as_view()),
    path('users/create', UserAPIView.as_view()),
    path('users/info', ProfileInfoAPIView.as_view()),
    path('users/password', ProfilePasswordAPIView.as_view()),
    path('users',UserlistAPI.as_view()),

    path('permissions', PermissionAPIView.as_view()),

    path('roles', listroleview.as_view()),
    path('roles/create', RoleViewSet.as_view()),
    
    path('roles/<str:pk>', RoleViewSet.as_view()),

    
    # path('users', UserGenericAPIView.as_view()),
    
]