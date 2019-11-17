import asyncio
from test_generation import TestGeneration
from daemon import Daemon
from connected_node import ConnectedNode

if __name__ == "__main__":
    if len(Daemon.node.connected_nodes) == 0:
        Daemon.node.connected_nodes.append(ConnectedNode("127.0.0.1"))
    asyncio.run(Daemon.node.send_email("123abc", Daemon.node.get_public()))
    # asyncio.run(TestGeneration.send_out_transactions())