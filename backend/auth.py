import jwt
import datetime
import time
from jwt.exceptions import ExpiredSignatureError

# 全局密钥
secret = '12345678900'


# 生成token
def encode_func(user):
    dic = {
        'exp': datetime.datetime.now() + datetime.timedelta(days=1),  # 过期时间
        'iat': datetime.datetime.now() - datetime.timedelta(days=1),  # 开始时间
        'iss': 'qyh',  # 签发者
        'data': user
    }
    encoded = jwt.encode(dic, secret, algorithm='HS256')
    return encoded


# 解析token
def decode_func(token):
    decode = jwt.decode(token, secret, issuer='qyh', algorithms=['HS256'])
    print(decode)
    # 返回解码出来的data
    return decode['data']