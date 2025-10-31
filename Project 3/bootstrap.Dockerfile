FROM python:3.9-slim

# Sets up the application directory inside the container.
WORKDIR /app

# Copies your bootstrap server code into /app.
COPY bootstrap.py .

# Installs Flask — the only required dependency for your bootstrap node.
RUN pip install flask

# Optional but recommended) documents that your app listens on port 5000.
# Doesn’t actually open the port, but helps when linking containers via Docker Compose or networks.
EXPOSE 5000

# Tells Docker to start your bootstrap service automatically when the container runs.
CMD ["python", "bootstrap.py"]
