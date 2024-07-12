from django.urls import path
from api import views

urlpatterns = [
    path("auth/register", views.Register, name="Register"),
    path(
        "auth/verification-code/<str:token>",
        views.VerifyEmailTokenCode,
        name="VerifyEmailTokenCode",
    ),
]
