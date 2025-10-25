"""
Task 1: Anycast (TCP)
Description: This client connects to the service name "server" within the Docker Compose network. Each connection may reach a different server instance, demonstrating load-balanced "Anycast" behavior.
"""

import socket
import random
import time

SERVERS = ["172.19.0.2", "172.19.0.3", "172.19.0.4"]
PORT = 5000

def main():
    for attempt in range(3):
        server_ip = random.choice(SERVERS)
        print(f"[client] attempting connection to anycast -> {server_ip}:{PORT}")
        try:
            with socket.create_connection((server_ip, PORT), timeout=3) as sock:
                data = sock.recv(1024)
                print(f"[client] received: {data.decode()}")
        except Exception as e:
            print(f"[client] connection failed: {e}")
        time.sleep(1)

if __name__ == "__main__":
    main()

