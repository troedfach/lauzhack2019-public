from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
import hashlib
from Crypto import Random
from base64 import b64encode, b64decode
import hashlib

class Crypto:

    hash = "SHA-256"

    @staticmethod
    def newkeys(keysize):
        random_generator = Random.new().read
        key = RSA.generate(keysize, random_generator)
        private, public = key, key.publickey()
        return public, private
    @staticmethod
    def importKey(externKey):
        return RSA.importKey(externKey)
    @staticmethod
    def getpublickey(priv_key):
        return priv_key.publickey()
    @staticmethod
    def encrypt(message, pub_key):

        cipher = PKCS1_OAEP.new(Crypto.importKey(pub_key))
        value = message.encode('utf-8')

        return cipher.encrypt(value)
    @staticmethod
    def decrypt(ciphertext, priv_key):

        cipher = PKCS1_OAEP.new(priv_key)
        return cipher.decrypt(ciphertext)
    @staticmethod
    def sign(message, priv_key, hashAlg="SHA-256"):
        #global hash
        #hash = hashAlgs
        signer = PKCS1_v1_5.new(Crypto.importKey(priv_key))
        digest = SHA256.new()
        """if (hash == "SHA-512"):
            digest = SHA512.new()
        #elif (hash == "SHA-384"):
            digest = SHA384.new()
        #elif (hash == "SHA-256"):
        elif (hash == "SHA-1"):
            digest = SHA.new()
        else:
            digest = MD5.new()"""
        digest.update(message)
        return b64encode(signer.sign(digest))

    @staticmethod
    def verify(message, signature, pub_key):
        value = message.encode('utf-8')
        signer = PKCS1_v1_5.new(Crypto.importKey(pub_key))
        digest = SHA256.new()
        """if (hash == "SHA-512"):
            digest = SHA512.new()
        elif (hash == "SHA-384"):
            digest = SHA384.new()
        elif (hash == "SHA-256"):
        elif (hash == "SHA-1"):
            digest = SHA.new()
        else:
            digest = MD5.new()"""
        digest.update(value)
        return signer.verify(digest, b64decode(signature))

    @staticmethod
    def gen_hash(contents):
        try: 
            value = contents.encode('utf-8')
        except AttributeError:
            value = contents

        contents_hash = hashlib.sha512(value).hexdigest()
        return contents_hash



