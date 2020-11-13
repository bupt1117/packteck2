import jwt
import datetime
import logging
from django.conf import settings
from django.utils import timezone
from ..models import Rule


# 需要传入
def create_token(payload, timeout=60):
    salt = settings.SECRET_KEY

    # 构造header
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }

    # 其实就是往payload加入了有效时间
    payload['exp'] = datetime.datetime.now() + datetime.timedelta(minutes=timeout)  # 有效时间

    token = jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers).decode('utf-8')
    return token


def token_encode(token):
    token = token.encode('utf-8')
    payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
    return payload


def idmatch(token, rid):
    token_user = token_encode(token)
    ruleobject = Rule.objects.get(pk=rid)
    uid = token_user["user_id"]
    if ruleobject.uid.pk != uid:
        return False
    else:
        return True
