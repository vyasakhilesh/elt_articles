# Use the official Ubuntu image from the Docker Hub
FROM ubuntu:latest

# Update the package list and install required packages
RUN apt-get update && apt-get install -y sudo

# Add a new user (replace 'newuser' with your desired username)
# RUN useradd -ms /bin/bash airbyte

# Give the new user sudo privileges
RUN echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Switch to the new user
USER ubuntu

# Set the working directory
WORKDIR /home/ubuntu

RUN sudo apt-get update && \
    sudo apt-get install -y --no-install-recommends sudo ca-certificates curl && \
    sudo install -m 0755 -d /etc/apt/keyrings && \
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
    sudo chmod a+r /etc/apt/keyrings/docker.asc && \
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    sudo apt-get update

RUN sudo apt-get install -y --no-install-recommends \
    docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


RUN sudo groupmod -g 1001 docker
RUN sudo usermod -aG docker ubuntu
RUN sudo usermod -aG sudo ubuntu

# USER ubuntu
RUN curl -LsfS https://get.airbyte.com | bash -
# RUN sudo service docker start && sleep 10s
# RUN abctl local install
# RUN abctl local install --low-resource-mode --no-browser

# Default command (optional, replace with your desired command)
CMD ["tail", "-f", "/dev/null"]