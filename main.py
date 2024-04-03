##
## PERSONAL PROJECT, 2024
## my_honeypot
## File description:
## ssh honeypot
##

import argparse

from src.honeypot import run

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSH honeypot")
    parser.add_argument("--port", type=int, help="Port to listen on", default=2222)
    parser.add_argument("--ip", type=str, help="IP to listen on", default="0.0.0.0")
    run(parser.parse_args().ip, parser.parse_args().port, "key/host_key.pem")
    exit(0)