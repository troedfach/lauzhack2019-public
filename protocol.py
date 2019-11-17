import asyncio

class Protocol:
    @staticmethod
    async def publish_block(block, pow_hash):
        from daemon import Daemon
        # construct a message
        # broadcast it
        message = block.__dict__
        transactions = []
        for transaction in block.transactions:
            transactions.append(transaction.__dict__)

        message['id'] = 3
        message['pow_hash'] = pow_hash
        message['transactions'] = transactions
        await Daemon.send_message(message)
        return 0