"""
Организовать взаимодействие клиента и сервера:
клиент открывает файл (который вы создали и наполнили) и построчно читает и перекидывает по сети строки на сервер.
Сервер принимает строки и складывает их в новый файл, логируя время принятия.

Исходный файл:
123
456
789

Результирующий файл:
2021-06-09 21:49:54.657742 123
2021-06-09 21:49:54.657742 456
2021-06-09 21:49:54.657742 789
"""
import socket
import sys
from logging import getLogger, StreamHandler
from time import sleep

logger = getLogger(__name__)
stdout_handler = StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logger.setLevel("DEBUG")

sock = socket.create_connection(('127.0.0.1', 10002), timeout=5)

with sock:
    with open('incoming.txt', 'r') as f_obj:
        for line in f_obj.readlines():
            data = line.strip().encode('utf-8')
            sock.sendall(data)
            logger.info(f'data: {data}')
            sleep(1)