from datetime import datetime
import jwt


class TokenHandler:
    def __init__(self, secret_key, expire_time):
        self.secret_key = secret_key
        self._algorithm = "HS256"
        self.expire_time = expire_time

    def create_access_token(self, username):
        jwt_data_to_encode = {'username': username}
        expire = datetime.utcnow() + self.expire_time

        jwt_data_to_encode.update({"exp": str(expire)})
        encoded_jwt = jwt.encode(jwt_data_to_encode,
                                 self.secret_key,
                                 algorithm=self._algorithm)
        return encoded_jwt

    def verify_token(self, token):
        header_data = jwt.get_unverified_header(token)
        # using that variable in the decode method
        if jwt.decode(
            token,
            key=self.secret_key,
            algorithms=[header_data['alg'], ]
        ):
            return True
        return False
