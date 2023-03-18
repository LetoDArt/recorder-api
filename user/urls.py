from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CustomUserCreate, BlacklistTokenUpdateView, CustomUserGet

app_name = 'users'

urlpatterns = [
    path('signup', CustomUserCreate.as_view(), name="create_user"),
    path('logout', BlacklistTokenUpdateView.as_view(), name='blacklist'),
    path("login", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh", TokenRefreshView.as_view(), name='token_refresh'),
    path("user/current", CustomUserGet.as_view(), name='current_user'),
]
