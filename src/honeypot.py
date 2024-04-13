##
## PERSONAL PROJECT, 2024
## my_honeypot
## File description:
## honeypot class
##

from os import remove
import socket
import threading
import paramiko

from src.get_infos_user import get_infos_user

SSH_BANNER = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"


def run(ip: str, port: int, key_path: str) -> None:
    host_key = paramiko.RSAKey(filename=key_path)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen(100)
    print(f"Listening for connection on {ip}:{port}")
    while True:
        client, addr = sock.accept()
        threading.Thread(target=handle_connection, args=(client, host_key, addr)).start()


def handle_connection(conn, host_key, addr):
    from src.Honeypotclass import Honeypot

    transport = paramiko.Transport(conn)
    transport.add_server_key(host_key)
    transport.local_version = SSH_BANNER
    server = Honeypot(22, "0.0.0.0", "key/host_key.pem", addr[0])
    try:
        transport.start_server(server=server)
        infos, address = get_infos_user(addr[0])
        server.logger.log_info(f"Got a connection from {addr[0]}:{addr[1]}")
        server.logger.log_info(f"Infos for client {addr[0]}: {infos} - {address}")
    except paramiko.SSHException as e:
        print(f"SSH negotiation failed: {e}")
        return
    handle_chan(transport, addr, server)


def handle_chan(transport: paramiko.Transport, addr: tuple, server):
    command_text = ""
    chan = transport.accept(10)
    if chan is None:
        print("*** No channel (from " + addr[0] + ").")
        raise Exception("No channel")
    chan.settimeout(100)
    chan.send("Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-128-generic x86_64)\r\n")
    chan.send("$: ")
    while True:
        try:
            command = chan.recv(1024)
            chan.send(command)
            command_text += command.decode("utf-8")
            command_text = server.handle_commands(command_text, chan, addr[0])
            if not command:
                break
        except Exception as e:
            print(f"Error: {e}")
            break
