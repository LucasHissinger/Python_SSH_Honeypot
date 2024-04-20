##
## PERSONAL PROJECT, 2024
## my_honeypot
## File description:
## sys_func
##

import paramiko
import os


def check_binary(binary: str) -> bool:
    if os.path.exists("/usr/bin/" + binary) and os.path.isfile("/usr/bin/" + binary):
        return True
    return False


def my_exit(chan: paramiko.Channel) -> str:
    chan.send("\r\nConnection closed (via exit command)\r\n")
    chan.close()
    return ""


def my_id(chan: paramiko.Channel) -> str:
    return "\r\nuid=1000(user) gid=1000(user) groupes=1000(user)"


def my_ls(chan: paramiko.Channel) -> str:
    return "\r\nBureau\r\nDocuments\r\nImages\r\nMusique\r\nVidéos\r\nWork"


def my_cd(chan: paramiko.Channel) -> str:
    return "\r\nchanged directory with success"


def my_pwd(chan: paramiko.Channel) -> str:
    return "\r\n/home/user"


commands = {"ls\r": my_ls, "id\r": my_id, "cd\r": my_cd, "pwd\r": my_pwd, "exit\r": my_exit}
