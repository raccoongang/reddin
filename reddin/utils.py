import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESCipher:
    def __init__(self, key):
        self.bs = 32
        # str(): YAML-based deployment config may turn an all-digit key into an int
        self.key = str(key).encode('utf-8')

    def encrypt(self, raw):
        # pad the encoded bytes, not the str: non-ASCII chars are multi-byte
        cipher = AES.new(self.key, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(pad(raw.encode('utf-8'), self.bs)))

    def decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(base64.b64decode(enc)), self.bs).decode('utf-8')
