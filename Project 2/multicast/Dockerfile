# Dockerfile for Multicast sender/receiver with tcpdump preinstalled
FROM python:3.10-slim

WORKDIR /app

# Install tcpdump so containers can monitor UDP traffic
RUN apt-get update && apt-get install -y tcpdump

# Copy sender and receiver scripts
COPY multicast_sender.py /app/multicast_sender.py
COPY multicast_receiver.py /app/multicast_receiver.py

# Default behavior (can be overridden in docker-compose)
CMD ["python", "multicast_sender.py"]
