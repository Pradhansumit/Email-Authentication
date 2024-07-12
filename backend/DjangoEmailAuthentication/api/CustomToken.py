import secrets
import jwt
import time
import os
from dotenv import main
from datetime import timedelta, datetime, timezone

main.load_dotenv()


def CreateToken(user: dict):
    secret = os.getenv('secret')
    algorithm = os.getenv('algorithm')
    user_dtl = user
    payload = {
        'first_name': user_dtl["first_name"],
        'last_name': user_dtl["last_name"],
        'phone': user_dtl["phone"],
        'email': user_dtl["email"],
        'exp': datetime.now(timezone.utc) + timedelta(seconds=20)
    }

    token = jwt.encode(payload, secret, algorithm)
    return token
