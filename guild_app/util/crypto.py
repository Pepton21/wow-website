import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

    # constructor receives secret phrase
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    # convert string to bytes
    def str_to_bytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    # add PKCS7 padding
    def __add_padding(self, text):
        length = self.bs - (len(text) % self.bs)
        text += chr(length) * length
        return text

    # remove PKCS7 padding
    def __remove_padding(self, text):
        text = text[:-ord(text[-1])]
        return text

    # ecnrypt plaintext
    def encrypt(self, raw):
        raw = self.__add_padding(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    # decrypt ciphertext
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.__remove_padding(cipher.decrypt(enc[AES.block_size:]).decode('utf-8'))