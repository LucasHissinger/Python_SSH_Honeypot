
# Python_SSH_Honeypot

Implementation of the Paramiko library in python in order to code a simple SSH honeypot supporting authentication and a fake shell with basic commands. All of the flow of user is tracked and write in a log file


## Run Locally

Clone the project

```bash
  git clone https://github.com/LucasHissinger/my_honeypot.git
```

Go to the project directory

```bash
  cd my_honeypot
```

Install dependencies

```bash
  pip install -r requirements.txt
```
Create the ssh key for the server ssh

  ```bash
    ssh-keygen -t rsa -f key/host_key.pem
  ```

Launch the docker with the script run

```bash
  chmod +x run.sh
  ./run.sh
```

To check if the docker is successfully launched use

```bash
  docker ps
```
 and you will see a container named "fake_ssh"

## To add creds to the honeypot
To add creds to the honeypot modify the file "authorized_creds" in the key folder and add the creds you want to use in the following format :

```bash
  username:password:content_of_key_user.pub
```

## How to use
Launch the project and connect to the honeypot with the following command

```bash
  ssh username@ip_of_the_docker
```
or (dont forget to use chmod 400 on your key)
```bash
  ssh -i user_key username@ip_of_the_docker
```

And after that you can check the logfile in the app folder in the container

  ```bash
    docker exec -it fake_ssh /bin/bash
    cat honeypot.log
  ```

## Running Tests

To run tests, go to the root of the repo and run the following command

```bash
  chmod +x run_tests
  ./run_tests
```
## New features

### Get information about the user

This feature will allow the honeypot to get information about the user connected to the honeypot and write it in the log file when
the user is connected.
The information will be the following :

- country : country of the user
- countryCode : country code associated with the country
- region: region Code of the user
- regionName: region name of the user
- city: city of the user
- zip: zip code of the user
- lat: latitude of the user
- lon: longitude of the user
- isp: internet service provider of the user

Next, with the geopy.geocoders library, we will be able to get more infos about the geographical location of the user.
The infos will be:

- address: address of the user
- city: city of the user
- state: state of the user
- country: country of the user

Display the information in the log file in the following format :

address, city, state, country

### Logging system
The logs are in the logs folder and are architecture as follows :
```bash
logs
├── 127.0.0.1
│   ├── honeypot_2024-04-14 22:22:16.log
│   └── honeypot_2024-04-14 22:22:24.log
└── 34.35.36.37
    ├── honeypot_2024-04-14 23:22:18.log
    └── honeypot_2024-04-14 23:34:45.log
```

The logging system works as follows:
- When the user connects to the honeypot, the honeypot will write create a log file named with the date of the creation of the user sessions in the folder named by the ip of the user.

- The logging system will create a log file by session, if someone connects to the honeypot and disconnects and reconnects, the honeypot will create a new log file for the new session.

- you can erase one folder of logs by running the project with the following command:
```bash
  python main.py --port=port --delete-logs=ip
```

- you can erase all the logs with the following command:
```bash
  python main.py --port=port --delete-all-logs
```

- or using the script delete_logs.sh
```bash
  ./delete_logs.sh [<ip> | all]
```

## Documentation

Some documentation about the lib of the project and helpful links

#### Libs :
[Paramiko](https://linktodocumentation)

[Pytest](https://linktodocumentation)

#### other links :
[What is SSH](https://www.youtube.com/watch?v=Atbl7D_yPug)

[SSH implementation in python](https://www.youtube.com/watch?v=HO1h57CiF98)
## Feedback

If you have any feedback, please reach out to us at lucas.hissinger@epitech.eu


## Authors

- [@LucasHissinger](https://github.com/LucasHissinger)
