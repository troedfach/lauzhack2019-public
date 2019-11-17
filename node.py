from transaction import Transaction

import os
import platform
from node_crypto import Crypto
from base64 import b64encode, b64decode
from block import Block
import asyncio
from chain import Chain
from verification import Verification
import time
import json
from protocol_parameters import ProtocolParameters


class Node:
    def __init__(self):
        self.connected_nodes = []
        self.pubkey = ""
        self.current_block = Block()
        self.get_private()
        self.pubkey = self.get_public()
        self.contacts = []

    async def get_email(self, reader, writer):
        data = await reader.read(4096)
        data = data.split(b"\x0d\x0a\x0d\x0a")[1]
        print("Data: {}".format(data))
        t = json.loads(data)
        print(f'Received: {t!r}')
        await self.send_email(t['body'], t['email'])
        await writer.drain()
        writer.close()
        return 0

    
    async def listen_for_emails(self):
        host = '127.0.0.1'
        server = await asyncio.start_server(self.get_email, host, ProtocolParameters.email_port)
        await server.serve_forever()
        
    async def send_email(self, contents, destination):
        # encrypt
        # then sign
        # the broadcast
        with open("/etc/blockmail/" + destination) as f:
            destination = f.read()
        encrypted = Crypto.encrypt(contents, destination)
        encrypted = b64encode(encrypted)
        signature = Crypto.sign(encrypted, self.privkey)
        encrypted = encrypted.decode("utf-8")
        signature = signature.decode("utf-8")
        print("encrypted: {}".format(len(encrypted)))
        print("sig: {}".format(len(signature)))
        transaction_hash = Crypto.gen_hash(self.pubkey + destination + encrypted + signature)
        await self.broadcast(self.pubkey, destination, encrypted, signature, transaction_hash)


    def participate_in_consensus(self):
        # hmm
        return 0

    def generate_block(self):
        # takes all transaction broadcasts
        # verifies and adds to block

        return 0


    async def broadcast(self, sender, destination, contents, signature, contents_hash):
        from daemon import Daemon
        t = Transaction(sender, destination, contents, signature, contents_hash, time.time())
        message = t.__dict__
        message['id'] = 1
        await Daemon.send_message(message)


    @staticmethod
    def check_file():
        if platform.system() == 'Windows':
            path = "C:\\Program Files\\blockmail\\.priv"
            try:
                with open(path) as f:
                    return True
            except Exception:
                    return False
            return False

        else:
            path = "/etc/blockmail/.priv"
            try:
                with open(path) as f:
                    return True
            except Exception:
                    return False
            return False

    @staticmethod
    def create_file():
        email_address = "gwion.lly@gmail.com"
        if platform.system() == 'Windows':       
            public,private = Crypto.newkeys(2048)
            f = open("C:\\Program Files\\blockmail\\.priv","wb")
            f.write(private.exportKey())
            f.close()
            g = open("C:\\Program Files\\blockmail\\.pub","wb")
            g.write(public.exportKey())
            g.close()
            #await Node.post_public(public, email_address)
        else:
            public,private = Crypto.newkeys(2048)
            # TODO: fix when dir doesn't exit
            with open("/etc/blockmail/.priv","wb") as f:
                f.write(private.exportKey())
                f.close()
            g = open("/etc/blockmail/.pub","wb")
            g.write(public.exportKey())
            g.close()
            #await Node.post_public(public,email_address)

    #Make function to store public keys matching emails
    @staticmethod
    async def post_public(public,email_address):
        from daemon import Daemon
        message = {}
        message['id'] = 2
        message['pubkey'] = public
        message['email_address'] = email_address
        # need to do this whole daemon thing async
        await Daemon.send_message(message)
        return True

    #Make a function to get the public key
    """@staticmethod
    def get_public(email_address):
        return "a"""

    @staticmethod
    def get_public():
        if Node.check_file():
            if platform.system() == 'Windows':
                f = open("C:\\Program Files\\blockmail\\.pub","r")
                ret = f.read()
                f.close()
                return ret
            else:
                f = open("/etc/blockmail/.pub","r")
                ret = f.read()
                f.close()
                return ret
        else:
            Node.create_file()
            Node.get_public()

    def receive_email(self, email_text):
        if self.check_file():
            if platform.system() == 'Windows':
                return b64decode(Crypto.decrypt(email_text,self.privkey))
            else:
                return b64decode(Crypto.decrypt(email_text,self.privkey))

        else:
            self.create_file()
            self.receive_email(email_text)


    """def send_email(self, email_address,email_text):
        base_email = b64encode(email_text)
        public = self.get_public(email_address)
        return Crypto.encrypt(base_email,public)"""


    def get_private(self):
        if self.check_file():
            if platform.system() == 'Windows':
                f = open("C:\\Program Files\\blockmail\\.priv","r")
                self.privkey = f.read()
                f.close()
            else:
                f = open("/etc/blockmail/.priv","r")
                self.privkey = f.read()
                f.close()
        else:
            Node.create_file()
            self.get_private()
            
    def append_transaction(self, transaction):
        self.current_block.transactions.append(Transaction(transaction['sender'], transaction['destination'], transaction['contents'], transaction['signature'], transaction['contents_hash'], time.time()))

    def add_pubkey(self, broadcast):
        self.contacts.append((broadcast['pubkey'], broadcast['email_address']))
        with open("/etc/blockmail/" + broadcast['email_address'], "w") as f:
            f.write(broadcast['pubkey'])

        return 0

    def verify_block(self, block):
        # what the fuck
        new_block = Block()
        new_block.transactions = []
        for t in block['transactions']:
            t_new = Transaction(t['sender'], t['destination'], t['contents'], t['signature'], t['contents_hash'], t['timestamp'])
            new_block.transactions.append(t_new)
        new_block.timestamp = block['timestamp']
        new_block.previous_hash = block['previous_hash']
        new_block.nonce = block['nonce']
        new_block.block_hash = block['block_hash']
        new_block.pow_hash = block['pow_hash']
        if Verification.verify_all_signatures(new_block):
            Chain.add_block(new_block)
            return True
        else:
            return False

    def parse_broadcast(self, broadcast):
        if broadcast['id'] == 1:
            self.append_transaction(broadcast)
        elif broadcast['id'] == 2:
            self.add_pubkey(broadcast)
        else:
            if self.verify_block(broadcast):
                dec = Crypto.decrypt(b64decode(broadcast['transactions'][0]['contents']), Crypto.importKey(self.privkey))
                print(dec)
            else:
                print("validation failed")

        return 0


    
    async def mine_blocks(self, difficulty):
        while True:
            self.current_block = Block()
            self.current_block.transactions = []
            await self.current_block.mine_block(difficulty)
            # Chain.add_block(self.current_block)



    


