# Base image containing Python.
FROM python:3.9-slim 

# Set working directory.
WORKDIR /app

# copy your script inside the container.
COPY p2p_node.py .

# install Flask dependency.
RUN pip install flask requests 

EXPOSE 5000

# start the Python app when the container runs.
ENTRYPOINT ["python", "p2p_node.py"]
