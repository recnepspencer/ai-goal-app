"""
URL configuration for commitment_app project.

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
from django.urls import path
from .views.user_registration_view import UserRegistrationView
from .views.goal_creation_view import GoalCreationView
from .views.goal_completion_view import GoalCompletionView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Default JWT login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh token
    path('create-goal/', GoalCreationView.as_view(), name='goal-creation'),
    path('goals/<int:goal_id>/complete/', GoalCompletionView.as_view(), name='goal-completion'),
]


# path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # For login
# path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # For refreshing the token