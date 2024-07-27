import jwt
from api import models
from api.CustomToken import (
    CreateEmailToken,
    GetNewAccessToken,
    SetTokenAfterLogin,
    ValidateToken,
)
from api.serializer import UserSerializer
from api.VerficationMail import send_Verification_email
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from DjangoEmailAuthentication import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
            tk_result = ValidateToken(token=kwargs.get("token"))
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


# RESET PASSWORD EMAIL
@api_view(["POST"])
def ResetPasswordEmail(request, *args, **kwargs) -> Response:
    if request.method == "POST":
        email_rec: str = request.data.get("email")

        user_model: models.CustomUser = models.CustomUser.objects.get(email=email_rec)

        if user_model is not None:

            user: dict[str, str] = {
                "first_name": user_model.first_name,
                "last_name": user_model.last_name,
                "phone": user_model.phone_number,
                "email": email_rec,
            }

            token: str = CreateEmailToken(user=user)

            # sending mail to the user with token
            sub: str = "Password Reset"
            msg: str = "Click in the link below to reset your password"
            rec_list = email_rec
            html_msg = f"""
                    <html>
                        <head>
                            <style>
                            a{{
                                padding:7px 10px;
                                font-size:20px;
                                background-color: #00C000;
                                color:white;
                                border:none;
                                outline:none;
                                cursor:pointer;
                                border-radius:5px;
                            }}
                            </style>
                        </head>
                        <body>
                            <div>
                            <p>Please click on the button below to change you password.</p>
                            <a href="http://localhost:5173/auth?token={token}">Click Me</a>
                            </div>
                        </body>
                    </html>
                    """
            send_mail(
                subject=sub,
                message=msg,
                from_email="bitsj2022060577@bitbaroda.com",
                recipient_list=[rec_list],
                html_message=html_msg,
            )
            return Response(status=status.HTTP_200_OK)


# VALIDATE TOKEN FOR RESETTING PASSWORD
@api_view(["POST"])
def ResetPasswordTokenValidation(request):
    if request.method == "POST":
        token = request.data.get("token")

        try:
            if token is not None:
                tk_result = ValidateToken(token)
                if tk_result == True:
                    return Response(
                        data={"successful": "Token Accepted"},
                        status=status.HTTP_202_ACCEPTED,
                    )
                else:
                    return Response(
                        data={"error": "Token Invalid"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        except Exception as ex:
            return Response({"error": str(ex)}, status=500)


# CHANGE PASSWORD
@api_view(["POST"])
def ResetForgetPassword(request):
    try:
        if request.method == "POST":
            password: str = request.data.get("password")
            confirm_password: str = request.data.get("confirm_password")
            token: str = request.data.get("token")

            # validation for token and passwords
            if not password or not confirm_password or not token:
                return Response(
                    {"message": "All fields are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if password != confirm_password:
                return Response(
                    {"message": "Passwords do not match"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # jwt requirements from settings.py file
            secret = settings.JWT_SECRET
            algorithm = settings.JWT_ALGORITHM

            # jwt validation
            try:
                token_dec = jwt.decode(token, secret, algorithms=[algorithm])
            except jwt.ExpiredSignatureError:
                return Response(
                    {"message": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST
                )
            except jwt.InvalidTokenError:
                return Response(
                    {"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
                )

            user_email = token_dec.get("email")
            if not user_email:
                return Response(
                    {"message": "Invalid token payload"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # email validation from db
            try:
                user_model = models.CustomUser.objects.get(email=user_email)
            except models.CustomUser.DoesNotExist:
                return Response(
                    {"message": "User does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_model.set_password(password)
            user_model.save()

            return Response(
                {"successful": "Password has been changed"}, status=status.HTTP_200_OK
            )

    except Exception as e:
        # Log the exception if needed
        print(f"An error occurred: {e}")
        return Response(
            {"message": "An error occurred"}, status=status.HTTP_400_BAD_REQUEST
        )
