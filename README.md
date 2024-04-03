
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
  username:password:content_of_key.pub
```

## How to use
Launch the project and connect to the honeypot with the following command

```bash
  ssh username@ip_of_the_docker
```
or
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
