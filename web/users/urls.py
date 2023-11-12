from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import PasswordResetEmailView, PasswordResetOtpView, LogoutView, UserProfileView, VerifyView, RegisterView, LoginView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='signup'),
    path('verify/', VerifyView.as_view(), name='confirm'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path("reset-password-email/", PasswordResetEmailView.as_view(), name="send otp to email"),
    path("reset-password-code/", PasswordResetOtpView.as_view(), name="write otp with new password"),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
]

