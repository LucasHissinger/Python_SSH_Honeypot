FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install iptables
RUN apt update -y && apt-get install iptables sudo -y

# Make port 22 available to the world outside this container
EXPOSE 22

CMD [ "python", "./main.py", "--port=22"]
