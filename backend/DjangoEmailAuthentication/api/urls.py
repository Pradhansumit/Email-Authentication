from django.urls import path

from . import views

urlpatterns = [
    path('Register', views.UserProfileListCreateView.as_view(), name="hello-world"),
    path('token', views.CustomTokenObtainPairView.as_view(), name="token"),
    path('sendMail', views.sendMail)
]
