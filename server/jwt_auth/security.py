
import datetime
import pytz
import jwt
from dotenv import load_dotenv
import os 

load_dotenv()


class Security():

    secret = os.getenv('JWT_KEY')
    tz = pytz.timezone("America/Caracas")

    @classmethod
    def generateNewToken(cls, authenticatedUser):
        accessPayload = {
            'iat': datetime.datetime.now(tz=cls.tz),
            'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=3),
            'id_user': authenticatedUser['idusuario'],
            'user_name': authenticatedUser['nombre']
        }
        
        refreshPayload = {
            'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(days=90)
        }

        return {'ACCESS_TOKEN': jwt.encode(accessPayload, cls.secret, 'HS256'),
                'REFRESH_TOKEN': jwt.encode(refreshPayload, cls.secret, 'HS256')}
    
    @classmethod
    def refreshToken(cls, prevRefreshToken):
        pass