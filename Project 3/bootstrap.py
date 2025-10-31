# Imports Flask for web server functionality, request for incoming POST data, and jsonify for formatting JSON responses.
from flask import Flask, request, jsonify

app = Flask(__name__) # Initializes the Flask app.
registered_peers = set() # registered_peers is a Python set() to store unique peer URLs (avoiding duplicates).

# Root endpoint to confirm the bootstrap node is running.
@app.route('/')
def index():
    return jsonify({"message": "Bootstrap node is running!"}) # Returns JSON text message.

# Handles registration of peers.
@app.route('/register', methods=['POST'])
def register():
    peer = request.json.get("peer") 
    if peer:
        registered_peers.add(peer) # Adds valid peers to the registered_peers set.
        return jsonify({"status": "registered", "peer": list(registered_peers)}) # Returns a success JSON if added
    return jsonify({"error": "No peer provided"}), 400 # or return error code 400 if "peer" missing.

# Converts set → list because JSON doesn’t support sets.
@app.route('/peers', methods=['GET']) #GET info from reg. peers 
def get_peers():
    return jsonify({"peers": list(registered_peers)}) # Returns the list of all registered peers.

if __name__ == '__main__': # Runs the Flask app, listening on port 5000 and all network interfaces.
    app.run(host='0.0.0.0', port=5000) # In Docker, 0.0.0.0 is necessary so the service is reachable from other containers.
