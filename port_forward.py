#!/usr/bin/python3
import argparse
import select
import socket
from sys import exit
import threading

def verify_port(port: str) -> int:
    if int(port) > 65535 or int(port) < 1:
        print(f"[!] Invalid Port provided: {port}")
        exit(1)
    return int(port)

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lport", "-l", type=verify_port, required=True)
    parser.add_argument("--dport", "-d", type=verify_port, required=True)
    parser.add_argument("--target", "-t", type=str, required=True)
    parser.add_argument("--server", "-s", type=str, required=True)
    return parser.parse_args()     


def client(conn, addr):
    print(f"[*] Incoming Connection from {addr[0]}:{addr[1]}")
    READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
    READ_WRITE = READ_ONLY | select.POLLOUT
    TIMEOUT = 100
    out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    out.connect((args.target, args.dport))
    out.setblocking(0)
    
    poller = select.poll()
    poller.register(conn, READ_WRITE)
    poller.register(out, READ_WRITE)
    fd_to_socket = {conn.fileno(): conn, out.fileno(): out}
    while True:
        events = poller.poll(TIMEOUT)
        
        for fd, flag in events:
            s = fd_to_socket[fd]
            if flag & (select.POLLIN | select.POLLPRI):
                data = s.recv(1024)
                if data:
                    if s is conn:
                        print(f"[*] Sent {len(data)} bytes to target")
                        out.sendall(data)
                    elif s is out:
                        print(f"[*] Sent {len(data)} bytes to client")
                        conn.sendall(data)
                else:
                    return

if __name__ == "__main__":
    args = init_args()

    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.bind((args.server, args.lport))
    serv_sock.listen(5)

    while True:
        conn, addr = serv_sock.accept()
        threading.Thread(target=client, args=(conn, addr)).start()
