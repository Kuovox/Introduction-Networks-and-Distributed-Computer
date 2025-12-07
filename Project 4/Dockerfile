# Simple Dockerfile for a single P2P/DHT node
FROM python:3.11-slim

# Install basic system deps (optional, but often useful)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Storage directory inside container
RUN mkdir -p /app/storage

# Environment defaults (can be overridden)
ENV PORT=5000

EXPOSE 5000

CMD ["python", "app.py"]
