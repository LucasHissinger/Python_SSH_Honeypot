#!/bin/bash

# Run the application
docker stop fake_ssh
docker rm -f fake_ssh
docker build -t basic_honeypot .
docker run -d --cap-add=NET_ADMIN --name fake_ssh basic_honeypot