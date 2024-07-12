from .serializer import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .CustomToken import CreateToken


@api_view(['POST'])
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
            print(token)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
