##
## PERSONAL PROJECT, 2024
## Python_SSH_Honeypot
## File description:
## status_type
##

from enum import Enum


class Status(Enum):
    COMPLETE = "log completed, session terminated"
    USED = "Used by someone"
    OTHER = "Other status"
