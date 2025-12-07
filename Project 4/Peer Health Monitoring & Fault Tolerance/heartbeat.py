from flask import Flask, request, jsonify, send_from_directory
import os, requests, threading, time, sys

app = Flask(__name__)
STORAGE_DIR = "./storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

#key-value store
kv_store = {}

# peer list
peers = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003"
]

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(STORAGE_DIR, file.filename))
    return jsonify({"status": "uploaded", "filename": file.filename})

#download file and saves in storage folder
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(STORAGE_DIR, filename, as_attachment=True)


#heartbeat
@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({"status": "alive"}), 200


@app.route('/add_peer', methods=['POST'])
def add_peer():
    peer = request.json.get("peer")
    if peer and peer not in peers:
        peers.append(peer)
    return jsonify({"status": "peer added", "peers": peers})

def monitor_peers(): #checking for periodic heartbeat
    global peers
    while True:
        alive = []
        for peer in peers:
            try:
                res = requests.get(f"{peer}/heartbeat", timeout=2)
                if res.status_code == 200:
                    alive.append(peer)
            except:
                print(f"Peer {peer} is unresponsive")
        peers = alive #update list 
        time.sleep(5)


if __name__ == "__main__":
    #allow port to be passed as argument 
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

    #peer monitoring thread
    threading.Thread(target=monitor_peers, daemon=True).start()
    app.run(host="0.0.0.0", port=port)
