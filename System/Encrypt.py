from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os


class Encrypt:
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('KEY')

    def encrypt(self, bottle):
        fernet = Fernet(self.key)
        encrypted = fernet.encrypt(bottle.encode())
        return encrypted