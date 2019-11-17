import json
import sys
import socket

#HOST = '127.0.0.1'
HOST = '192.168.43.234'
PORT = 2525


contents = sys.argv[1]
with open("/etc/blockmail/jorge@sigint.mx") as f:
    destination = f.read()

d = {}
d['contents'] = contents
d['destination'] = destination

data = json.dumps(d)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(data.encode("utf-8"))

