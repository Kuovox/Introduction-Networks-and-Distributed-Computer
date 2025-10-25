"""
Task 2: Multicast (UDP)
Decription: This receiver joins a multicast group (224.1.1.1:5007), listens for messages for a specified duration, and prints them. It supports both UTF-8 JSON and binary messages.
"""

import socket
import struct
import argparse
import time
import json

# Multicast group and port
GROUP = '224.1.1.1'
PORT = 5007

def receive(duration=10): # Joins a multicast group and receives messages for a fixed duration.
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Allow multiple receivers to bind the same address/port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', PORT))

    # Join multicast group
    mreq = struct.pack('4sL', socket.inet_aton(GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    print(f"[RECEIVER] Joined multicast group {GROUP}:{PORT} for {duration} seconds.")

    sock.settimeout(1.0)
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            data, addr = sock.recvfrom(65536)
            try:
                # Attempt to decode as UTF-8 text
                decoded = data.decode()
                print(f"[RECEIVER] From {addr}: {decoded}")

                # Try to parse JSON if applicable
                try:
                    obj = json.loads(decoded)
                    print("  Parsed JSON:", obj)
                except json.JSONDecodeError:
                    pass
            except UnicodeDecodeError:
                # Fallback for binary data
                print(f"[RECEIVER] Binary data from {addr}: {data.hex()}")

        except socket.timeout:
            continue

    print("[RECEIVER] Leaving multicast group.")
    sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multicast Receiver")
    parser.add_argument('--duration', type=int, default=10, help="Listening duration in seconds")
    args = parser.parse_args()
    receive(duration=args.duration)
