import qrcode
import jwt
import time
from typing import Final


class QRGenerator:
    def __init__(self):
        self.base_url = 'http://api.lotuss.everyresearch.com/APIs/newBottleTransaction'
        from System.Mac import get_mac_address
        self.secret = str(get_mac_address())
        self.machineID: Final[str] = '1'

    def generate_qr(self, bottle):
        query_params = {'points': bottle,
                        'iat': time.time()}
        jwt_token = self.gen_jwt_token(query_params)

        qr = qrcode.QRCode(version=3, box_size=2, border=10, error_correction=qrcode.constants.ERROR_CORRECT_H)
        url_to_query = self.base_url + '?' + 'data=' + jwt_token + '&machineIDin=' + self.machineID
        qr.add_data(url_to_query)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")

    def gen_jwt_token(self, data: dict):
        token = jwt.encode(data, self.secret, algorithm='HS256')
        return token
