'''
Citation(s):
1) “Generating Random id’s using UUID in Python.” GeeksforGeeks, 04 Apr 2025.
2) “How to Build a Flask Python Web Application from Scratch.” DigitalOcean, updated December 12 2024.
3) “Flask HTTP methods, handle GET & POST requests.” GeeksforGeeks, Last Updated 23 Jul 2025.
'''

import sys # read command-line arguments (port).
import threading # used later for periodic peer refreshes (you prepared for future use).
import time # used later for periodic peer refreshes (you prepared for future use).
import requests # to send HTTP requests to bootstrap or peers.
import uuid # to generate a unique node ID.
import os
from flask import Flask, request, jsonify # to create a lightweight web API.

app = Flask(__name__)
node_id = str(uuid.uuid4()) # uniquely identifies the node.
peers = set() # stores known peer URLs.

bootstrap_url = os.getenv("BOOTSTRAP_URL", "http://host.docker.internal:5000")  # points to the bootstrap node on the host machine (important for Docker).
port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000 # can be overridden via command-line, defaulting to 5000.
my_url = os.getenv("NODE_URL", f"http://host.docker.internal:{port}")

# register with bootstrap node
def register_with_bootstrap(port):
    """
    Builds the node’s own address (e.g., http://localhost:5001).
    Sends a POST request to bootstrap’s /register.
    Logs success or failure.
    flush=True ensures immediate console output (important inside Docker).
    """
    try:
        res = requests.post(f"{bootstrap_url}/register", json={"peer": my_url})
        if res.ok:
            data = res.json()
            peers.update(data.get("peers", []))
            print(f"[OK] Registered as {my_url}, peers: {peers}", flush=True)
        else:
            print(f"[ERR] Bootstrap returned {res.status_code}", flush=True)
    except Exception as e:
        print(f"[ERR] Registration failed: {e}", flush=True)

#discover peers from bootstrap
def discover_peers():
    """
    Gets the /peers list from the bootstrap node.
    Adds all peers except itself to the local peers set.
    Logs the list of peers found.
    """
    try:
        res = requests.get(f"{bootstrap_url}/peers")
        if res.ok:
            peer_list = res.json().get("peers", [])
            for peer in peer_list:
                if peer != my_url:
                    peers.add(peer)
            print(f"[INFO] Discovered peers: {peers}", flush=True)
    except Exception as e:
        print(f"[ERR] Discovery failed: {e}", flush=True)

def continuous_discovery(interval=10):
    while True:
        discover_peers()
        time.sleep(interval)

# receive and send message 
@app.route('/')
def index(): # Health check endpoint showing node’s unique ID.
    return jsonify({"message": f"Node {node_id} is running!"})

@app.route('/message', methods=['POST'])
def message():
    """
    receives messages from other nodes and logs them
    logs the message sender and contents 
    returns confirmation JSON { "status": "received" }.
    """
    data = request.json
    sender = data.get("sender")
    msg = data.get("msg")
    print(f"Received message from {sender}: {msg}", flush=True)
    return jsonify({"status": "received"})

#get peer list when requested 
@app.route('/peers', methods=['GET'])
def get_peers():
    return jsonify({"peers": list(peers)}) # Converts set → list for JSON serialization.

def send_message_to_peers(msg):
    for peer in list(peers):
        try:
            requests.post(f"{peer}/message", json={"sender": my_url, "msg": msg})
        except Exception as e:
            print(f"[WARN] Could not send to {peer}: {e}", flush=True)

if __name__ == '__main__':
    """
    First registers with the bootstrap node.
    Then fetches the current peer list.
    Starts Flask server accessible externally on port 5000 (inside the container).
    """
    register_with_bootstrap(port)
    threading.Thread(target=continuous_discovery, daemon=True).start()
    app.run(host='0.0.0.0', port=port)
    #start flask on all interfaces 0.0.0.0 

''' 
PHASE 1
import uuid
from flask import Flask, jsonify #jsonify for formatting 

app = Flask(__name__)
node_id = str(uuid.uuid4()) #unique identifier with uuid4 for random numbers

@app.route('/')
def index():
    return jsonify({"message": f"Node {node_id} is running!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
    # 0.0.0.0 listens to all
    # port 5000 is used in example 


when we need to run phase 1 again --> remove node 1 and then build again
docker rm node1
docker build -t p2p-node .
docker run -d -p 5000:5000 --name node1 p2p-node


PHASE 2 
import sys 
import uuid
from flask import Flask, request, jsonify #jsonify for formatting 

app = Flask(__name__)
node_id = str(uuid.uuid4()) #unique identifier with uuid4 for random numbers
peers = set() #store peer addr 

@app.route('/')
def index():
    return jsonify({"message": f"Node {node_id} is running!"})

@app.route('/register', methods=['POST'])
def register():
    peer = request.json.get("peer")
    if peer:
        peers.add(peer)
        return jsonify({"status": "registered", "peer": peer})
    return jsonify({"error"}), 400

@app.route('/message', methods=['POST'])
def message():
    data = request.json
    sender = data.get("sender")
    msg = data.get("msg")
    print(f"Received message from {sender}: {msg}", flush=True)
    return jsonify({"status": "received"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
    # 0.0.0.0 listens to all
    # port 5000 is used in example 
'''

'''
for ($i = 1; $i -le 7; $i++) {
    $port = 5000 + $i
    $nodeUrl = "http://node${i}:${port}"
    docker run -d --name node$i --network p2pnet `
        -p $port`:5000 `
        -e NODE_PORT=$port `
        -e NODE_URL=$nodeUrl `
        -e BOOTSTRAP_URL="http://bootstrap:5000" `
        p2p-node
}

for ($i = 1; $i -le 8; $i++) {
    $src = Get-Random -Minimum 1 -Maximum 8
    $dst = Get-Random -Minimum 1 -Maximum 8
    $srcPort = 5000 + $src
    $dstPort = 5000 + $dst
    Write-Host "Sending from node$src to node$dst"
    Invoke-WebRequest -Uri "http://localhost:$dstPort/message" -Method POST -ContentType "application/json" `
        -Body "{`"sender`": `"node$src`", `"msg`": `"Hello node$dst`"}"
}
'''