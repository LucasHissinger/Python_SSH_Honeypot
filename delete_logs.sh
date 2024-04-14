#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [<ip> | all]
    <ip> - the IP address of the device
    all  - delete all log folders in ./logs"
    exit 1
fi
if [ "$1" == "all" ]; then
    rm -rf ./logs/*
    echo "All folders in ./logs have been deleted."
    exit 0
fi

log_folder="./logs/$1"

if [ -d "$log_folder" ]; then
    rm -rf "$log_folder"
    echo "Log folder $log_folder has been deleted."
else
    echo "Log folder $log_folder does not exist."
fi
exit 0