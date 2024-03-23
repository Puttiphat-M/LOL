from dotenv import load_dotenv
import os


class Encrypt:
    def __init__(self):
        load_dotenv()
        key = os.getenv('KEY')
        self.n, self.e = [int(x, 16) for x in key.split(',')]

    def encrypt(self, bottle):
        encrypted_message = [pow(ord(char), self.e, self.n) for char in bottle]
        return encrypted_message


if __name__ == "__main__":
    encrypt = Encrypt()
    print(encrypt.encrypt("10"))