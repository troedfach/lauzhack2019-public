# set up a listener
# add transaction to block
# if block is not empty, mine for block
# sporadically send out transactions
from connected_node import ConnectedNode
from test_generation import TestGeneration
import asyncio
from daemon import Daemon

async def main():
    Daemon.node.connected_nodes.append(ConnectedNode('127.0.0.1'))
    Daemon.node.connected_nodes.append(ConnectedNode('192.168.43.234'))
    task1 = asyncio.create_task(Daemon.listen_for_transactions())
    task2 = asyncio.create_task(Daemon.node.listen_for_emails())
    task3 = asyncio.create_task(Daemon.node.mine_blocks(2))
    await task1
        # task2 = asyncio.create_task(TestGeneration.send_out_transactions())
    await task2
    await task3


if __name__ == "__main__":
    asyncio.run(main())




