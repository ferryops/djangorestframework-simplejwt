"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, LoginView, ProfileView, ContractView, TrainingScheduleView, DeleteUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<int:pk>', DeleteUserView.as_view(), name='user'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile_detail'),
    path('contracts', ContractView.as_view(), name='contracts'),
    path('contracts/<int:pk>/', ContractView.as_view(), name='contract-detail'),
    path('schedule/', TrainingScheduleView.as_view(), name='schedule'),
    path('schedule/<int:pk>/', TrainingScheduleView.as_view(), name='schedule-detail'),
]