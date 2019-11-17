import asyncio
import json
from node import Node
from protocol_parameters import ProtocolParameters
from transaction import Transaction
from connected_node import ConnectedNode

class Daemon:
    
    node = Node()

    @staticmethod
    async def deal_with_transactions(reader, writer):
        data = await reader.read(40960)
        t = json.loads(data)
        print(f'Received: {t!r}')
        Daemon.node.parse_broadcast(t)
        await writer.drain()
        writer.close()
        return 0

    @staticmethod
    async def listen_for_transactions():
        host = '0.0.0.0'
        server = await asyncio.start_server(Daemon.deal_with_transactions, host, ProtocolParameters.port)
        await Daemon.node.post_public(Daemon.node.pubkey, "gwion.lly@gmail.com")
        await server.serve_forever()

    @staticmethod
    async def send_message(message):
        # broadcasts need to have an id
        # 1: transaction
        # 2: public key publishing
        # 3: block registration
        print(message)
        message = json.dumps(message)
        for connected_node in Daemon.node.connected_nodes:
            while True:
                try:
                    _, writer = await asyncio.open_connection(connected_node.ip, ProtocolParameters.port)
                    break
                except ConnectionRefusedError:
                    await asyncio.sleep(3)

            print(f'Send: {message!r}')
            writer.write(message.encode())
            await writer.drain()

            writer.close()
            await writer.wait_closed()

# testing
"""
if __name__ == "__main__":
    # asyncio.run(Daemon.listen_for_transactions())
    Daemon.node.connected_nodes.append(ConnectedNode('127.0.0.1'))
    t = Transaction("s", "d", "a", "b", "c", time.time())
    message = {}
    message['id'] = 1
    message['transaction'] = json.dumps(t.__dict__)
    asyncio.run(Daemon.send_message(t))"""

    