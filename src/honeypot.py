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
import logging

from src.sys_func import commands, check_binary
from src.get_infos_user import get_infos_user

SSH_BANNER = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"


if open("honeypot.log", "w"):
    remove("honeypot.log")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="honeypot.log",
)


def handle_commands(commend_text: str, chan: paramiko.Channel, username: str):
    if commend_text[-1] == "\r":
        logging.warning(f"command : {commend_text.replace(chr(13), '')} by ip {username}")
        if commend_text in commands:
            chan.send(commands[commend_text](chan))
        else:
            if check_binary(commend_text.split(" ")[0].replace(chr(13), "")):
                chan.send(
                    f"\r\n$: you're not authorized to use {commend_text.split(' ')[0].replace(chr(13), '')} on workspace"
                )
            else:
                chan.send(
                    f"\r\n$: {commend_text.split(' ')[0].replace(chr(13), '')}: command not found"
                )
        chan.send("\r\n$: ")
        return ""
    return commend_text


def run(ip: str, port: int, key_path: str) -> None:
    host_key = paramiko.RSAKey(filename=key_path)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen(100)
    logging.info(f"Listening for connection on {ip}:{port}")
    while True:
        client, addr = sock.accept()
        logging.info(f"Got a connection from {addr[0]}:{addr[1]}")
        infos, address = get_infos_user(addr[0])
        logging.info(f"Infos for client {addr[0]}: {infos} - {address}")
        threading.Thread(target=handle_connection, args=(client, host_key, addr)).start()


def handle_connection(conn, host_key, addr):
    from src.Honeypotclass import Honeypot

    transport = paramiko.Transport(conn)
    transport.add_server_key(host_key)
    transport.local_version = SSH_BANNER
    server = Honeypot(22, "0.0.0.0", "key/host_key.pem", addr[0])
    try:
        transport.start_server(server=server)
    except paramiko.SSHException as e:
        print(f"SSH negotiation failed: {e}")
        return
    handle_chan(transport, addr)


def handle_chan(transport: paramiko.Transport, addr: tuple):
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
            command_text = handle_commands(command_text, chan, addr[0])
            if not command:
                break
        except Exception as e:
            print(f"Error: {e}")
            break
