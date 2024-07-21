import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "6f8632261860cdc4a6aed3683dbf12093202b6ad3fa9dc8dec427c752002a82b"  

def create_access_token(user_id: str, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = {'user_id': user_id}
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        expiration_time = datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc)
        if expiration_time >= datetime.now(timezone.utc):
            return decoded_token
        else:
            return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
