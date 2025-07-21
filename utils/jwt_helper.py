import jwt
import datetime
from flask import current_app

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 1시간 후 만료
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    return token
