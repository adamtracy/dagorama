# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install Graphviz
RUN apt-get update && apt-get install -y graphviz

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

RUN chmod +x install.sh && ./install.sh

# See docker-compose.yml for the command to run the container
