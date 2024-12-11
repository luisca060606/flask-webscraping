import datetime
import jwt
import pytz


class Security():
    # config secret jwt in config file
    secret = "asdf67asdfh(@/-ds"
    tz = pytz.timezone("America/Caracas")

    @classmethod
    def generate_token(cls, authenticated_user):
        payload = {
            'iat': datetime.datetime.now(tz=cls.tz),
            'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=100),
            'email': authenticated_user.user_email,
            'roles': ['Administrator', 'Editor']
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")
    
    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            try:
                payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
                roles = list(payload['roles'])
                if 'Administrator' in roles:
                    return True
                return False
            except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                return False
        return False