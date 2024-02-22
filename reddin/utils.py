import base64

from Crypto.Cipher import AES


class AESCipher:
    def __init__(self, key):
        self.bs = 32
        self.key = key

    def encrypt(self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self.key.encode('utf-8'), AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return self._unpad(cipher.decrypt(enc))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]
