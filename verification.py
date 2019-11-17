from chain import Chain
import time
from node_crypto import Crypto

class Verification:
    def __init__(self):
        self.previous_time = self.get_previous_time()
    def parse_block(self,block):
        return 1
    @staticmethod
    def verify_all_signatures(block):
        from node import Node
        transactions = block.transactions
        final = ""
        for trn in transactions:
            public = Node.get_public()# trn.sender)
            if not Crypto.verify(trn.contents,trn.signature,public):
                print("verify")
                print("{}\n {}\n {}".format(trn.contents, trn.signature, public))
                print("{}\n {}\n {}".format(len(trn.contents), len(trn.signature), len(public)))
                return False
            if Crypto.gen_hash(str(trn.sender)+str(trn.destination)+str(trn.contents)+str(trn.signature)) != trn.contents_hash:
                print("transaction hashes")
                return False
            final += str(trn.__dict__)
        final += str(block.timestamp)
        final += block.previous_hash
        final += str(block.nonce)
        if Crypto.gen_hash(final) != block.block_hash:
            print("final hash")
            return False
        return True

    def verify_timestamp(self,block):
        if block.timestamp >= self.previous_time and block.timestamp < time.time():
            return True
        else:
            return False
    @staticmethod
    def get_previous_time():
        if len(Chain.blocks) == 0:
            return 0
        else:
            return Chain.blocks[-1].timestamp
        