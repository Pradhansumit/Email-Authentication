import jwt
import os
from dotenv import main
from datetime import timedelta, datetime, timezone
from api import models

main.load_dotenv()


def CreateToken(user: dict) -> str:
    secret = os.getenv("secret")
    algorithm = os.getenv("algorithm")
    user_dtl = user
    payload = {
        "first_name": user_dtl["first_name"],
        "last_name": user_dtl["last_name"],
        "phone": user_dtl["phone"],
        "email": user_dtl["email"],
        "exp": datetime.now(timezone.utc) + timedelta(seconds=20),
    }

    token = jwt.encode(payload, secret, algorithm)

    tokenModel = models.TokenModel()
    tokenModel.token = token
    tokenModel.user = user_dtl["email"]
    tokenModel.save()
    return token
