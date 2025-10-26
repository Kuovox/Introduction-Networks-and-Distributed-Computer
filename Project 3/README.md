# CECS 327 – Project 3: A Bite of Peer-to-Peer

**Group Members:**
- Khoa Vu (030063200)
- Kelly Pham (03039600)

---

## Project Overview
This project implements a **peer-to-peer (P2P)** distributed network using **Docker containers** and **Python (Flask)**.  
Each node acts as both a client and a server, registering with a central bootstrap node, discovering peers, and exchanging messages directly.

### Learning Outcomes
- Understand P2P network architecture and bootstrap-based peer discovery.  
- Use Docker to containerize and simulate dozens of nodes.  
- Implement peer registration, discovery, and message passing in Flask.

---

## Folder Structure

Project 3/

├── README.md

└── p2p-system/

├── bootstrap.py

├── bootstrap.Dockerfile

├── p2p_node.py

└── Dockerfile

---

## How to Build and Run

### Step 1: Create a Docker Network
All containers must share a virtual network to communicate.
```bash
docker network create p2p-net
```

---

### Step 2: Build Bootstrap and Node Images
```bash
docker build -t bootstrap-node -f bootstrap.Dockerfile .
docker build -t p2p-node .
```

---

### Step 3: Run the Bootstrap Node
Start the bootstrap server on port 5000.
```bash
docker run -d --name bootstrap --network p2p-net -p 5000:5000 bootstrap-node
```
Verify it’s running:
```bash
curl http://localhost:5000/
# {"message": "Bootstrap node is running!"}
```

---

### Step 4: Launch Multiple P2P Nodes
The following loop spins up 30 nodes (each bound to a unique port).
Powershell
```powershell
for ($i = 1; $i -le 30; $i++) {
    $port = 5000 + $i
    docker run -d --name node$i --network p2p-net `
        -p $port:5000 `
        -e NODE_URL="http://node$i:5000" `
        -e BOOTSTRAP_URL="http://bootstrap:5000" `
        p2p-node
}
```
Bash (Linux / macOS / WSL)
```bash
for i in $(seq 1 30); do
    port=$((5000 + i))
    docker run -d --name node$i --network p2p-net \
        -p $port:5000 \
        -e NODE_URL="http://node$i:5000" \
        -e BOOTSTRAP_URL="http://bootstrap:5000" \
        p2p-node
done
```
Check that containers are active:
```bash
docker ps
```
Each node registers with the bootstrap node and logs its peer list.

---

### Step 5: Simulate Peer-to-Peer Messaging
Use a second loop to send messages between random nodes.
Powershell
```powershell
for ($j = 1; $j -le 20; $j++) {
    $src = Get-Random -Minimum 1 -Maximum 30
    $dst = Get-Random -Minimum 1 -Maximum 30
    if ($src -ne $dst) {
        Write-Host "Sending from node$src to node$dst"
        $dstPort = 5000 + $dst
        Invoke-WebRequest -Uri "http://localhost:$dstPort/message" `
            -Method POST -ContentType "application/json" `
            -Body "{`"sender`": `"node$src`", `"msg`": `"Hello node$dst`"}" | Out-Null
    }
}
```
Bash (Linux / macOS / WSL)
```bash
for j in $(seq 1 20); do
    src=$((RANDOM % 30 + 1))
    dst=$((RANDOM % 30 + 1))
    if [ $src -ne $dst ]; then
        echo "Sending from node$src to node$dst"
        dstPort=$((5000 + dst))
        curl -s -X POST http://localhost:$dstPort/message \
            -H "Content-Type: application/json" \
            -d "{\"sender\": \"node$src\", \"msg\": \"Hello node$dst\"}" | jq .
        sleep 0.3
    fi
done
```
Expected output:
```bash
Sending from node12 to node8
{
  "status": "received"
}
Sending from node3 to node25
{
  "status": "received"
}
```

---

### Step 6: Inspect Logs
Check any node’s console output:
```bash
docker logs node8 | tail
# [MSG] From node12: Hello node8
```

---

### Cleanup After Testing

Stop and remove all containers and networks to reset your environment.
```bash
# Stop all containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -aq)

# Delete the custom network
docker network rm p2p-net

# Optional: Remove images to free space
docker rmi p2p-node bootstrap-node
```

---

### Expected Learning Outcomes
- Implement a containerized P2P network using Flask and Docker.
- Understand peer registration and discovery via a bootstrap node.
- Observe inter-node communication across 30 nodes in real time.
- Gain hands-on experience with Docker networking and multi-container deployment.
- Perform proper cleanup and resource management after testing.
