##
## PERSONAL PROJECT, 2024
## my_honeypot
## File description:
## class
##

import paramiko

from src.sys_func import commands, check_binary
from src.Loggerclass import Logger


class Honeypot(paramiko.ServerInterface):
    def __init__(self, port: int, ip_serv: str, host_key_filename: str, ip_client: str) -> None:
        self.logger = Logger(ip_client)
        self.port = port
        self.ip_serv = ip_serv
        self.ip_client = ip_client
        self.host_key = paramiko.RSAKey(filename=host_key_filename)
        self.authorized_passwords = {}
        self.authorized_keys = {}
        with open("key/authorized_creds", "r") as f:
            for lines in f.readlines():
                user, password, key = lines.split(":")
                self.authorized_passwords[user] = password
                self.authorized_keys[user] = key.split(" ")[1]

    def __repr__(self) -> str:
        return f"honeypot({self.port}, {self.ip})"

    def check_channel_request(self, kind: str, chanid: int) -> int:
        self.logger.log_info(
            f"client called check_channel_request ({self.ip_client}) with kind {kind} and chanid {chanid}"
        )
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        return True

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        return True

    def check_channel_exec_request(self, channel, command):
        command_text = str(command.decode("utf-8"))
        self.logger.log_info(
            f"client called check_channel_exec_request ({self.ip_client}) with command {command_text}"
        )
        return True

    def check_auth_password(self, username: str, password: str) -> int:
        self.logger.log_info(
            f"client called check_auth_password ({self.ip_client}) with username {username} and password {password}"
        )
        if username in self.authorized_passwords:
            if password == self.authorized_passwords[username]:
                self.logger.log_info(f"password authentication successful for {username}")
                return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "publickey,password, none"

    def check_auth_publickey(self, username, key):
        self.logger.log_info(
            f"client called check_auth_publickey ({self.ip_client}) with username {username} and key {key.get_name()} "
        )
        self.logger.log_info(f"content of key: {key.get_base64()}")
        if username in self.authorized_keys:
            if key.get_base64() in self.authorized_keys[username]:
                self.logger.log_info(f"public key authentication successful for {username}")
                return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def handle_commands(self, commend_text: str, chan: paramiko.Channel, username: str):
        if commend_text[-1] == "\r":
            self.logger.log_warning(
                f"command : {commend_text.replace(chr(13), '')} by ip {username}"
            )
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
