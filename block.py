from node_crypto import Crypto
import asyncio
from protocol import Protocol
from chain import Chain
import time
class Block:
    # block body consists of:
    # transaction, hash and signature of each transaction
    # should we split block body and block hash
    def __init__(self, transactions = [], timestamp = 0, previous_hash = "", nonce = ""):
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def hash_block(self, nonce):
        contents = self.previous_hash + str(self.timestamp)
        for transaction in self.transactions:
            contents += transaction.contents
            contents += transaction.contents_hash
            contents += transaction.signature

        contents += nonce
        return Crypto.gen_hash(contents)


    async def mine_block(self, difficulty):
        while len(self.transactions) == 0:
            await asyncio.sleep(5)
        nonce = 0
        while (self.hash_block(str(nonce))[0:difficulty] != "0"*difficulty):
            nonce += 1
            await asyncio.sleep(0.01)
        pow_hash = self.hash_block(str(nonce))
        self.nonce = nonce

        if len(Chain.blocks) != 0:
            self.previous_hash = Chain.blocks[-1].block_hash
            
        block_string = ""
        for t in self.transactions:
            # print("str trn: {}".format(str(t)))
            block_string += str(t.__dict__)

        self.timestamp = time.time()
        block_string += str(self.timestamp)
        block_string += str(self.previous_hash)
        block_string += str(self.nonce)

        self.block_hash = Crypto.gen_hash(block_string)

        await Protocol.publish_block(self, pow_hash)

        return (pow_hash, nonce)
        







