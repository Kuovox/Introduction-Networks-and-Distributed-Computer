# CECS 327 – Project 4: Distributed Hash Table Storage System

**Group Members:**
- Khoa Vu (030063200)
- Kelly Pham (03039600)

---

## Project Overview
This project implements a Distributed Hash Table (DHT) system using Python (Flask) and Docker, where multiple nodes cooperate to:
- Upload and download files
- Store and retrieve key–value pairs
- Distribute data across nodes using consistent hashing
- Forward requests to the correct node in the P2P ring

Each node in the system acts as an independent storage server with its own local file directory and in-memory key–value store. Nodes communicate with each other using HTTP and determine responsibility for a key using SHA-1 hashing.

---

## Learning Objectives
Through this project, students will learn:
- How distributed storage systems assign responsibility using DHTs
- How consistent hashing enables scalable, fault-tolerant systems
- How to containerize multiple cooperating nodes using Docker
- How to implement simple message forwarding between peer nodes
- How peer configuration and routing work in distributed systems

---

## System Features
1. File Upload & Download
Each node exposes endpoints to store and retrieve files from its local storage directory:
- `POST /upload` – Upload a file to this node
- `GET /download/<filename>` – Download a stored file

Storage directories are persisted using Docker volumes.

2. Key–Value Store
Nodes maintain a lightweight key–value dictionary:
- `POST /kv` – Store a `"key": "value"` pair
- `GET /kv/<key>` – Retrieve a stored value

However, keys are not stored on the node that receives the request. Instead, the system uses the DHT ring to determine where each key should be stored.

3. DHT Routing
The DHT routing uses:
- SHA-1 hashing over node URLs to determine ring positions
- SHA-1 hashing over keys to determine responsible node
- Forwarded requests using Flask + Python `requests` library

If a node receives a request for a key that belongs to another node, it automatically forwards the request to the correct peer.

4. Environment-Based Configuration
Each container uses:
- `SELF_URL` – the node’s own address
- `PEERS` – list of all peer URLs in the network
- `PORT` – service port (default 5000)

This makes the system fully configurable and scalable to more nodes.

--- 

## Folder Structure
```nginx
Project 4/
│
├── app.py                # Main Flask application
├── Dockerfile            # Container image definition
├── docker-compose.yml    # Multi-node orchestration
├── requirements.txt      # Python dependencies
└── storage/              # Node-local storage (Docker volume)
```

---

## How to Build and Run the System
1. Ensure Docker is Installed
   
Windows users should run through WSL2 Ubuntu for best compatibility.

2. Navigate to the Project Director
```bash
cd /mnt/c/Users/...
```

3. Build and Start All Nodes
```bash
docker compose up --build
```
This launches three nodes:
| Node  | URL                                    | Localhost Port                                 |
| ----- | -------------------------------------- | ---------------------------------------------- |
| node1 | [http://node1:5000](http://node1:5000) | [http://localhost:5001](http://localhost:5001) |
| node2 | [http://node2:5000](http://node2:5000) | [http://localhost:5002](http://localhost:5002) |
| node3 | [http://node3:5000](http://node3:5000) | [http://localhost:5003](http://localhost:5003) |

---

## Testing the System
1. Check Node Health
```bash
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
```

2. Upload a File
```bash
curl -X POST -F "file=@test.txt" http://localhost:5001/upload
```

3. Download a File
```bash
curl -O http://localhost:5001/download/test.txt
```

4. Store a Key
```bash
curl -X POST http://localhost:5001/kv \
  -H "Content-Type: application/json" \
  -d '{"key":"color","value":"blue"}'
```
Even if you send the request to node1, the value may be stored on node2 or node3 depending on SHA-1 hashing.

5. Retrieve a Key
```bash
curl http://localhost:5002/kv/color
```
If node2 is not responsible for `"color"`, the request is forwarded automatically.

--- 

## Understanding the DHT Ring

Each node computes:
```text
node_id = SHA1(node_url)
key_id  = SHA1(key)
```
Role of the ring:
- Sort node_ids in ascending order
- Responsible node = first node whose id ≥ key_id
- Wrap around to the first node if no match
  
This ensures predictable placement and load distribution.

--- 

## Cleanup
To stop and remove all containers:
```bash
docker compose down
```

To remove images:
```bash
docker rmi project4-node
```

---

## Expected Learning Outcomes

After completing this project, you should understand:
- How distributed systems coordinate storage
- How DHTs support scalable lookup and routing
- How to forward messages between nodes
- How Docker simulates distributed systems on a single machine
- How consistent hashing avoids hotspots and rebalancing issues
