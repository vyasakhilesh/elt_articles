FROM ubuntu:latest

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends sudo ca-certificates curl && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update

RUN apt-get install -y --no-install-recommends \
    docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# USER ubuntu
RUN curl -LsfS https://get.airbyte.com | bash -
RUN sudo service docker start && sleep 10s
# RUN abctl local install
# ADD https://github.com/airbytehq/abctl/releases/download/v0.24.0/abctl-v0.24.0-linux-amd64.tar.gz abctl.tar.gz
# RUN tar -xvzf abctl.tar.gz -C .
# RUN chmod +x abctl*/abctl
# RUN sudo mv abctl /usr/local/bin
# RUN abctl local install --low-resource-mode
# RUN abctl local credentials
# -c', 'sudo docker run hello-world'
EXPOSE 8000

CMD ["tail", "-f", "/dev/null"]