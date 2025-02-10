FROM ubuntu:latest

# Update the package list and install sudo
RUN apt-get update && \
    apt-get install -y sudo

# Use a non-root user to run commands
RUN useradd -ms /bin/bash airbyte && \
    echo 'airbyte:airbyte' | chpasswd && \
    usermod -aG sudo airbyte

# Allow the non-root user to use sudo without a password
RUN echo 'airbyte ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Switch to the non-root user
USER airbyte
RUN sudo apt-get update && \
    sudo apt-get install -y --no-install-recommends ca-certificates curl && \
    sudo install -m 0755 -d /etc/apt/keyrings && \
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
    sudo chmod a+r /etc/apt/keyrings/docker.asc && \
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo  tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    sudo apt-get update

RUN sudo apt-get install -y --no-install-recommends \
    docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

EXPOSE 8000

CMD ["tail", "-f", "/dev/null"]