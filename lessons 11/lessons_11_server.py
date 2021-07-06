import datetime
import socket
import sys
from logging import getLogger, StreamHandler

logger = getLogger(__name__)
stdout_handler = StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logger.setLevel("DEBUG")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 10002))
sock.listen(socket.SOMAXCONN)

conn, addr = sock.accept()

with conn, sock:
    while True:
        data = conn.recv(1024)
        if not data:
            print('Ничего нет')
            break
        with open('outgoing.txt', 'a', encoding='utf-8') as f_obj:
            print(f'{datetime.datetime.now()}: {data.decode("utf-8")}', file=f_obj)
            logger.info('received data: {data}')