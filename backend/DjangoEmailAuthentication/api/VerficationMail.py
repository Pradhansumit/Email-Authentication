from django.core.mail import send_mail
from rest_framework import status


def send_Verification_email(token: str, email: str, first_name: str):
    """
    send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
    """
    sub = "Verify your account"
    msg = f"Hello, {first_name}"
    rec_list = email
    html_msg = f'<p>Verify your account using this verification code: <a href="http://localhost:8000/api/auth/verification-code/{token}">Verify</a></p>'
    send_mail(
        subject=sub,
        message=msg,
        from_email="bitsj2022060577@bitbaroda.com",
        recipient_list=[rec_list],
        html_message=html_msg,
    )
    return status.HTTP_200_OK
