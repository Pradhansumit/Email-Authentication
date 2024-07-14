from api.serializer import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.CustomToken import CreateToken, GetToken
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
            token = CreateToken(user)
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
    except Exception as ex:
        return Response({"error": str(ex)}, status=500)


@api_view(["POST"])
def Logout(request, *args, **kwargs):
    try:
        if request.user.is_authenticated():
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

            # print(f"\n\n username= {user_name} \t password = {user_pass} \n\n")

            user = authenticate(request, username=user_name, password=user_pass)
            print(f"\n\n \t\t {user} \n\n")

            if user is not None:
                login_result = login(request, user)

                # print(f"\n\n \t\t {login_result} \n\n")
                # user_details = CustomUser.objects.get(email=user_name)

                return Response(
                    data={"message": "Login successful"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data={"message": "Invalid username or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
    except Exception as ex:
        return Response(
            {"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
