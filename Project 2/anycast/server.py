"""
Task 1: Anycast (TCP)
Description: This server runs inside a Docker container and listens for incoming TCP client connections on port 5000. Multiple copies of this same container are launched (3 in total), each responding with its own unique message. When a client connects, Docker's internal DNS/load-balancer randomly routes the connection to one server instance,
simulating an "Anycast" setup.

Citation(s):
1) DigitalOcean. (2025, February 21). Python Socket Programming: Server and Client Example Guide. Retrieved from https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client#https://www.geeksforgeeks.org/python/how-to-capture-udp-packets-in-python/#
2) GeeksforGeeks — “How to Capture UDP Packets in Python” GeeksforGeeks. (2025, July 23). How to Capture UDP Packets in Python. Retrieved from https://www.geeksforgeeks.org/python/how-to-capture-udp-packets-in-python/
"""

# Host and Port Configuration
import socket
import os

HOST = "0.0.0.0"
PORT = 5000

def main():
    server_name = os.getenv("HOSTNAME", "unknown-server")
    print(f"[{server_name}] starting server on port {PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"[{server_name}] connection from {addr}")
                message = f"Hello from {server_name}"
                conn.sendall(message.encode())
                print(f"[{server_name}] sent: {message}")

if __name__ == "__main__":
    main()



