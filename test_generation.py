import asyncio
from transaction import Transaction
import json
from daemon import Daemon
import time

class TestGeneration:
    @staticmethod
    async def send_out_transactions():
        for i in range(100):
            # should move this somewhere else
            print("Sending out transaction: {}".format(i))
            t = Transaction(str(i), "d", "a", "b", "c", time.time())
            message = t.__dict__

            message['id'] = 1
            # message['transaction'] = t.__dict__
            await Daemon.send_message(message)
            await asyncio.sleep(5)

