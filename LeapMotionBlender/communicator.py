import bpy
import queue
import threading
import asyncio

import socket
import json 

from aiohttp.web import TCPSite
from .socket_server import server_thread_starter

wserver = None
running  = False
message_queue = queue.Queue()
server_port = 0

def start_server(host, port):
    global running
    global wserver
    if wserver:
        return (False, "The server is already running")

    if is_port_open(host,port):
        return (False, "The port is not open")
    wserver = threading.Thread(target=server_thread_starter, args=(host,port,))
    wserver.daemon = True
    wserver.start()
    global server_port 
    server_port = port
    return (True, "Server started at port: {}".format(port))

def clear_queue():
    global message_queue
    with message_queue.mutex:
        message_queue.queue.clear()

def force_start(host, port):
    newport = port if is_port_open(host,port) else get_open_port()
    (did_start, reason) = start_server(host, newport)

    return (did_start, reason, newport)

def get_open_port():
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("",0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port  

def is_port_open(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False
