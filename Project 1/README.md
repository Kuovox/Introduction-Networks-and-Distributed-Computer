# CECS 327 – Project 1: Docker Containers

**Group Members:**
- Khoa Vu (030063200)
- Kelly Pham (03039600)

## Project Overview
This project demonstrates the use of Docker to:
1. Run simple containers (Alpine, Python).
2. Deploy a custom Python application inside a container.
3. Deploy an Nginx web server with a custom index.html page.
4. Create a multi-container setup (server + multiple clients) using Docker Compose.

---

## Folder Structure
project/
├── docker-compose.yml
├── server/
│   ├── server.py
│   └── Dockerfile
├── client/
│   ├── client.py
│   └── Dockerfile
└── index.html   (for Nginx task)

---

## How to Build and Run

### Step 1: Download the "Project 1.zip"
Once downloaded, unzip the file and proceed to open the terminal within Project 1 folder.

### Step 2: Build and run the multi-container setup
docker compose up --build

Expected output:

- Server prints: Server listening on port 5000
- Clients print: Received from server: Server received your TCP message!

### Step 3: Stop Everything
If your terminal is still streaming logs, press:
CTRL + C

Then clean up containers:
docker compose down

### Step 4: Run Nginx web server
docker run -d -p 8080:80 -v ${PWD}/index.html:/usr/share/nginx/html/index.html nginx:latest
Expected output:
- Open http://localhost:8080 in your browser.
- You should see: "Hello from my custom Nginx!"

### Step 5: Stop Containers
1) docker ps
2) docker stop <container_id>
3) docker rm <container_id> (optional)


OPTIONAL (for debugging):

### Step 1: Run only the server 
docker compose up server

### Step 2: Run an interactive client (optional)
docker compose run --rm client1
