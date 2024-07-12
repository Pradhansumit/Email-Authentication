import secrets
import jwt
import time
import os
from dotenv import main
from datetime import timedelta, datetime, timezone

main.load_dotenv()

secret = os.getenv('secret')
algorithm = os.getenv('algorithm')

payload = {
    'user_id': 'abc',
    'exp': datetime.now(timezone.utc) + timedelta(seconds=20)
}

token = jwt.encode(payload, secret, algorithm)

time.sleep(21)

print(jwt.decode(token, secret, algorithm))
