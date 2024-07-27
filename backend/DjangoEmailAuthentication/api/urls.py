from api import views
from django.urls import path

urlpatterns = [
    path("auth/register", views.Register, name="Register"),
    path(
        "auth/verification-code/<str:token>",
        views.VerifyEmailTokenCode,
        name="VerifyEmailTokenCode",
    ),
    path("auth/login", views.Login, name="Login"),
    path("auth/logout", views.Logout, name="Logout"),
    path("auth/refresh", views.RefreshToken, name="Refresh"),
    path("auth/password-reset", views.ResetPasswordEmail, name="PasswordReset"),
    path(
        "auth/verify-password-reset",
        views.ResetPasswordTokenValidation,
        name="PasswordResetVerification",
    ),
    path(
        "auth/password-reset-confirm",
        views.ResetForgetPassword,
        name="PasswordResetConfirm",
    ),
]
