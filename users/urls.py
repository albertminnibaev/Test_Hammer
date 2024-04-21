from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import UserListAPIView, UserUpdateAPIView, UserRetrieveAPIView, VerificationView, \
    UserAuthenticationView, ReferralView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user_list'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_get'),
    path('verify/', VerificationView.as_view(), name='verification'),
    path('auth/', UserAuthenticationView.as_view(), name='user_authentication'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('refer/', ReferralView.as_view(), name='get_refer'),
]
