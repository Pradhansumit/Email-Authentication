from datetime import datetime, timedelta, timezone

import jwt
from api import models
from DjangoEmailAuthentication import settings
from rest_framework import status

# GET JWT TOKEN SETTINGS FROM SETTINGS FILE
secret = settings.JWT_SECRET
algorithm = settings.JWT_ALGORITHM

# FOR CREATING TOKEN
def CreateEmailToken(user: dict) -> str:
    user_dtl = user
    payload = {
        "first_name": user_dtl["first_name"],
        "last_name": user_dtl["last_name"],
        "phone": user_dtl["phone"],
        "email": user_dtl["email"],
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
    }

    token = jwt.encode(payload, secret, algorithm)

    tokenModel = models.TokenModel()
    tokenModel.token = token
    tokenModel.user = user_dtl["email"]
    tokenModel.save()
    return token

# FOR DECODING TOKEN
def ValidateToken(token):
    try:
        token_rec = jwt.decode(token, secret, algorithm)
        if token_rec:  # for valid token also for checking if the expiry is not over

            tk_model = models.TokenModel
            tk_model_result = tk_model.objects.get(token=token) # check if the token is present in db

            tk_user = token_rec["email"]
            tk_user_verified = models.CustomUser.objects.get(email=tk_user) # check for user in db
            
            if tk_model_result.isVerified is not True:
                if tk_model_result and tk_user_verified:
                    """
                        for changing status of user
                        user is active when the token is valid 
                        both in time and model
                    """
                    tk_model_result.isVerified = True
                    tk_model_result.save() # to set token one time usage
                    
                    
                    if tk_user_verified.is_active is not True: 
                        '''
                        only when a user is activating
                        the account after registration
                        '''
                        tk_user_verified.is_active = True
                        tk_user_verified.save()

                    return True
                return False
            else:
                return False

    except jwt.ExpiredSignatureError as ex:
        raise Exception({"Token Expired!", status.HTTP_401_UNAUTHORIZED})

    except (
        jwt.InvalidTokenError,
        models.TokenModel.DoesNotExist,
        models.CustomUser.DoesNotExist,
    ) as ex:
        raise Exception({"Invalid token or user not found.", status.HTTP_403_FORBIDDEN})

    except Exception as ex:
        raise Exception(
            {f"Error decoding token: {str(ex)}", status.HTTP_406_NOT_ACCEPTABLE}
        )
        
# SETTING TOKEN AFTER LOGIN IN COOKIE
def SetTokenAfterLogin(user:dict[str, str]):
    try:
        user_dtl = user
        payload = {
        "first_name": user_dtl["first_name"],
        "last_name": user_dtl["last_name"],
        "email": user_dtl["email"],
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
        }
        refresh_token = jwt.encode(payload, secret, algorithm)
        access_token = jwt.encode(
            {
                "full_name":user_dtl["first_name"]+user_dtl["last_name"],
                "email":user_dtl["email"],
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            }, 
            secret,
            algorithm
        )
        return {"refresh-token":refresh_token, "access-token":access_token}
        
    except Exception as ex:
        raise Exception ({f"Error decoding token: {str(ex)}", status.HTTP_403_FORBIDDEN})

# FOR NEW ACCESS AND REFRESH TOKEN
def GetNewAccessToken(refresh_token):
    try:
        token_dec = jwt.decode(refresh_token, secret, algorithm)
        if(token_dec):
            tk_user = token_dec["email"]
            print(f"tk_user, {tk_user}")
            tk_user_verified = models.CustomUser.objects.get(email=tk_user)
            if tk_user_verified:
                tk_user_details:dict[str, str] = {
                    "first_name":tk_user_verified.first_name, 
                    "last_name":tk_user_verified.last_name,
                    "email":tk_user_verified.email
                }
                new_token =  SetTokenAfterLogin(tk_user_details)
                return new_token
    except Exception as ex:
        raise Exception(
            {f"Error decoding token: {str(ex)}", status.HTTP_406_NOT_ACCEPTABLE}
        )
