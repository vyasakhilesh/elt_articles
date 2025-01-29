# airflow/Dockerfile
FROM apache/airflow:2.10.4-python3.10

USER root

# Install dependencies
RUN apt-get update && \
    apt-get install -y unzip

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Set JAVA_HOME environment variable
# ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
# ENV PATH=$JAVA_HOME/bin:$PATH

USER airflow

# Copy DAGS
COPY dags/ /opt/airflow/dags/
