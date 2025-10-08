# CECS 327 – Project 2: A Bite of Distributed Communication

**Group Members:**
- Khoa Vu (030063200)
- Kelly Pham (03039600)

---

## Project Overview
This project demonstrates two distributed communication models implemented using **Docker**, **Python**, and **Docker Compose**:

1. **Anycast (TCP):**  
   Multiple servers listen on the same port, and a client connects to one of them at random (simulating network-level load balancing).

2. **Multicast (UDP):**  
   One sender broadcasts JSON and binary messages to multiple receivers that join a multicast group.

---

## Folder Structure
project/

├── anycast/

│   ├── server.py

│   ├── client.py

│   ├── Dockerfile

│   └── docker-compose.yml

├── multicast/

│   ├── multicast_sender.py

│   ├── multicast_receiver.py

│   └── docker-compose.yml

└── README.md

---

## How to Build and Run

### Step 1: Download and open the “Project 2.zip”
Unzip the file and open a terminal inside the **Project 2** folder.

---

### Step 2: Run the Anycast (TCP) Demo
```bash
cd anycast
docker compose build
docker compose up --scale server=3
```
Expected output:
- Each server prints:
  ```[server] listening on 0.0.0.0:5000```
- Client prints results similar to:
```vbnet
Received: Hello from server
Received: Hello from server
Received: Hello from server
```
(Each message may originate from a different server replica.)

To stop and clean up:
```bash
CTRL + C
docker compose down
```

---

### Step 3: Run the Multicast (UDP) Demo
```bash
cd ../multicast
docker compose build
docker compose up
```
Expected output:
- Sender prints:
```css
Sent JSON: {"sensor": "temp", "value": 23.5}
Sent binary blob
```
- Receivers print messages such as:
```csharp
Joined multicast group 224.1.1.1:5007
Received from ('172.x.x.x', 5007): {"sensor": "temp", "value": 23.5}
Leaving multicast group
```
Stop everything:
```bash
CTRL + C
docker compose down
```

---

### Step 4: Verify Network Traffic (tcpdump)
You can inspect UDP or TCP packets directly inside any running container.
```bash
docker exec -it <container_name> bash
apt-get update && apt-get install -y tcpdump
tcpdump -i eth0 udp port 5007 -vv     # For Multicast
tcpdump -i eth0 tcp port 5000 -vv     # For Anycast
```

---

### Optional: Run individual services
Run only one side for testing or debugging:
```bash
# Start only servers (3 replicas)
docker compose up --scale server=3 server

# Run client separately
docker compose run --rm client
```

---

### Cleanup
After testing, remove all containers and networks:
```bash
docker compose down --volumes --remove-orphans
```

---

### Expected Learning Outcomes
- Understand differences between Anycast (TCP) and Multicast (UDP) models.
- Observe how Docker Compose scaling can simulate multiple servers in one network.
- Use tcpdump to capture and analyze distributed communication traffic.
- Recognize UDP unreliability and multicast group join/leave behavior.
