# airflow/Dockerfile
FROM apache/airflow:2.10.4-python3.10

USER root

# Install dependencies
RUN apt-get update && \
    apt-get install -y unzip

# Install Docker CLI using the official Docker repository
RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y docker-ce-cli

# Set JAVA_HOME environment variable
# ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
# ENV PATH=$JAVA_HOME/bin:$PATH

USER airflow

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Copy DAGS
COPY dags/ /opt/airflow/dags/
