from .serializer import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .CustomToken import CreateToken
from .VerficationMail import send_Verification_email


@api_view(["POST"])
def Register(request):
    if request.method == "POST":
        user_email = request.data.get("email")
        user_fname = request.data.get("first_name")
        user_lname = request.data.get("last_name")
        user_phone = request.data.get("phone_number")
        user = {
            "first_name": user_fname,
            "last_name": user_lname,
            "phone": user_phone,
            "email": user_email,
        }
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            token = CreateToken(user)
            send_Verification_email(
                token=token, email=user_email, first_name=user_fname
            )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def VerifyEmailTokenCode(request, *args, **kwargs):
    if kwargs.get("token", None) is not None:
        print(kwargs["token"])
        return Response()
    # token = request.data.get("token")
