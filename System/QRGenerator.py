import os

import qrcode
import jwt
import time
from dotenv import load_dotenv


class QRGenerator:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv('GEN_QR_URL')
        self.secret = os.getenv('SECRET')

    def generateQR(self, bottle):
        query_params = {'points': bottle,               # Bottle number
                       'location': 'Africa',
                        'iat': time.time()}
        jwt_token = self.gen_jwt_token(query_params)

        qr = qrcode.QRCode(version=3, box_size=2, border=10, error_correction=qrcode.constants.ERROR_CORRECT_H)
        url_to_query = self.base_url + '?' + 'data=' + jwt_token
        qr.add_data(url_to_query)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")

    def gen_jwt_token(self, data:dict):
        token = jwt.encode(data, self.secret, algorithm='HS256')
        return token