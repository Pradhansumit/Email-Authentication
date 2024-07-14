from django.urls import path
from api import views

urlpatterns = [
    path("auth/register", views.Register, name="Register"),
    path(
        "auth/verification-code/<str:token>",
        views.VerifyEmailTokenCode,
        name="VerifyEmailTokenCode",
    ),
    path("auth/login", views.Login, name="Login"),
    path("auth/logout", views.Logout, name="Logout"),
]
