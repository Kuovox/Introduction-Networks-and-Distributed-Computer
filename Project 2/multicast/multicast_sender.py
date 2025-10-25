"""
Task 2: Multicast (UDP)
Description: This sender transmits both JSON and binary data to a multicast group. Receivers that have joined the group (224.1.1.1:5007) will receive these packets.
"""

import socket
import time
import json
import struct
import argparse

# Multicast group IP and port (must be within 224.0.0.0 – 239.255.255.255 range)
MULTICAST_GROUP = '224.1.1.1'
PORT = 5007

def send_messages(interval=1, count=5): #Sends JSON and binary packets to the multicast group.
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Set the Time-To-Live (TTL) to 1 so packets don't leave the local network
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    print(f"[SENDER] Sending {count} messages every {interval}s to {MULTICAST_GROUP}:{PORT}")

    for i in range(count):
        # Example JSON data (like a sensor reading)
        msg = json.dumps({"sensor": "temp", "value": 20 + i}).encode()
        sock.sendto(msg, (MULTICAST_GROUP, PORT))
        print("[SENDER] Sent JSON:", msg.decode())
        time.sleep(interval)

    # Send a final binary message to demonstrate handling multiple formats
    binary_data = b'\x00\x01\x02\x03'
    sock.sendto(binary_data, (MULTICAST_GROUP, PORT))
    print(f"[SENDER] Sent binary data: {binary_data.hex()}")

    sock.close()
    print("[SENDER] Finished sending messages.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multicast Sender")
    parser.add_argument('--interval', type=float, default=1.0, help="Interval between messages (sec)")
    parser.add_argument('--count', type=int, default=5, help="Number of messages to send")
    args = parser.parse_args()
    send_messages(interval=args.interval, count=args.count)
