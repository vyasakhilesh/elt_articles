# spark/Dockerfile
FROM bitnami/spark:latest

USER root
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Copy scripts
COPY scripts/ /opt/spark/scripts/
