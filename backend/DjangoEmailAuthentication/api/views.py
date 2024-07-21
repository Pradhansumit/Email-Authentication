from api.serializer import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.CustomToken import (
    CreateEmailToken,
    GetNewAccessToken,
    GetToken,
    SetTokenAfterLogin,
)
from api.VerficationMail import send_Verification_email
from django.contrib.auth import authenticate, login, logout


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
            token = CreateEmailToken(user)
            send_Verification_email(
                token=token, email=user_email, first_name=user_fname
            )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def VerifyEmailTokenCode(request, *args, **kwargs):
    try:
        if kwargs.get("token", None) is not None:
            tk_result = GetToken(token=kwargs.get("token"))
            if tk_result == True:
                return Response(
                    data={"successful": "Token Accepted"},
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                return Response(
                    data={"error": "Token Invalid"}, status=status.HTTP_400_BAD_REQUEST
                )
    except Exception as ex:
        return Response({"error": str(ex)}, status=500)


@api_view(["POST"])
def Logout(request, *args, **kwargs):
    try:
        logout(request)
        return Response({}, status=status.HTTP_200_OK)

    except Exception as ex:
        return Response(
            {"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def Login(request, *args, **kwargs):
    try:
        # isValid: bool = False
        if request.method == "POST":
            user_name = request.data.get("username")
            user_pass = request.data.get("password")

            user = authenticate(request, username=user_name, password=user_pass)

            if user is not None:
                login(request, user)

                user_details: dict[str, str] = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                }

                # user_details = CustomUser.objects.get(email=user_name)
                tokens: dict[str, str] = SetTokenAfterLogin(user=user_details)

                response = Response(
                    {
                        "message": "Login Successful",
                        "access-token": f"{tokens['access-token']}",
                        "refresh-token": f"{tokens['refresh-token']}",
                    },
                    status=status.HTTP_200_OK,
                )
                response.set_cookie(
                    key="refresh_token",
                    value=tokens["refresh-token"],
                    secure=False,
                    max_age=604800,  # 7 days
                )
                response.set_cookie(
                    key="access_token",
                    value=tokens["access-token"],
                    secure=False,
                    max_age=300,
                )

                return response
            else:
                return Response(
                    data={"message": "Invalid username or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
    except Exception as ex:
        return Response(
            {"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def RefreshToken(request, *args, **kwargs):
    if request.method == "POST":
        refresh_token = request.data.get("refresh")
        print("refreshToken:", refresh_token)
        tokens = GetNewAccessToken(refresh_token=refresh_token)
        response = Response(
            {
                "message": "Login Successful",
                "access-token": f"{tokens['access-token']}",
                "refresh-token": f"{tokens['refresh-token']}",
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh-token"],
            secure=False,
            max_age=604800,  # 7 days
        )
        response.set_cookie(
            key="access_token",
            value=tokens["access-token"],
            secure=False,
            max_age=300,
        )
        return response
