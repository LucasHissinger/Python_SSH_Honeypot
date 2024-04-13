##
## PERSONAL PROJECT, 2024
## my_honeypot
## File description:
## ssh honeypot
##

import argparse
import shutil
import os

from src.honeypot import run

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSH honeypot")
    parser.add_argument("--port", type=int, help="Port to listen on", default=2222)
    parser.add_argument("--ip", type=str, help="IP to listen on", default="0.0.0.0")
    parser.add_argument(
        "--delete-all-logs", help="Delete logs on start", default=False, action="store_true"
    )
    parser.add_argument("--delete-log", help="Delete log file with given ip", default="")
    args = parser.parse_args()

    if args.delete_all_logs:
        for directory in os.listdir("./logs/"):
            shutil.rmtree(f"./logs/{directory}")
    if args.delete_log:
        if os.path.exists(f"./logs/{args.delete_log}"):
            shutil.rmtree(f"./logs/{args.delete_log}")

    run(parser.parse_args().ip, parser.parse_args().port, "key/host_key.pem")
    exit(0)
