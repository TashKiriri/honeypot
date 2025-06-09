#!/usr/bin/env python3
"""
Basic Honeypot - Educational/Research Purpose Only
Simulates SSH, HTTP, and FTP services to log attacker behavior
"""

import socket
import threading
import datetime
import json
import os
from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler

class HoneypotLogger:
    def __init__(self, log_file="honeypot.log"):
        self.log_file = log_file
        
    def log_attempt(self, service, client_ip, data):
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "service": service,
            "client_ip": client_ip,
            "data": data
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        print(f"[{timestamp}] {service} attempt from {client_ip}: {data}")

class SSHHoneypot(BaseRequestHandler):
    def handle(self):
        logger = HoneypotLogger()
        client_ip = self.client_address[0]
        
        try:
            # Send SSH banner
            self.request.send(b"SSH-2.0-OpenSSH_7.4\r\n")
            
            # Receive data
            data = self.request.recv(1024).decode('utf-8', errors='ignore')
            logger.log_attempt("SSH", client_ip, data.strip())
            
            # Simulate failed authentication
            self.request.send(b"Permission denied (publickey,password).\r\n")
            
        except Exception as e:
            logger.log_attempt("SSH", client_ip, f"Error: {str(e)}")

class HTTPHoneypot(BaseRequestHandler):
    def handle(self):
        logger = HoneypotLogger()
        client_ip = self.client_address[0]
        
        try:
            data = self.request.recv(1024).decode('utf-8', errors='ignore')
            logger.log_attempt("HTTP", client_ip, data.strip())
            
            # Send basic HTTP response
            response = b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
            self.request.send(response)
            
        except Exception as e:
            logger.log_attempt("HTTP", client_ip, f"Error: {str(e)}")

class FTPHoneypot(BaseRequestHandler):
    def handle(self):
        logger = HoneypotLogger()
        client_ip = self.client_address[0]
        
        try:
            # Send FTP banner
            self.request.send(b"220 FTP Server ready.\r\n")
            
            while True:
                data = self.request.recv(1024).decode('utf-8', errors='ignore')
                if not data:
                    break
                    
                logger.log_attempt("FTP", client_ip, data.strip())
                
                # Basic FTP responses
                if data.upper().startswith("USER"):
                    self.request.send(b"331 Password required.\r\n")
                elif data.upper().startswith("PASS"):
                    self.request.send(b"530 Login incorrect.\r\n")
                else:
                    self.request.send(b"502 Command not implemented.\r\n")
                    
        except Exception as e:
            logger.log_attempt("FTP", client_ip, f"Error: {str(e)}")

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    allow_reuse_address = True

def start_honeypot_service(port, handler_class, service_name):
    try:
        server = ThreadedTCPServer(("0.0.0.0", port), handler_class)
        print(f"Starting {service_name} honeypot on port {port}")
        server.serve_forever()
    except Exception as e:
        print(f"Error starting {service_name} honeypot: {e}")

def main():
    print("Basic Honeypot Starting...")
    print("Press Ctrl+C to stop")
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Start honeypot services in separate threads
    services = [
        (2222, SSHHoneypot, "SSH"),    # SSH on non-standard port
        (8080, HTTPHoneypot, "HTTP"),  # HTTP on alternate port
        (2121, FTPHoneypot, "FTP")     # FTP on non-standard port
    ]
    
    threads = []
    for port, handler, name in services:
        thread = threading.Thread(
            target=start_honeypot_service,
            args=(port, handler, name)
        )
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    try:
        # Keep main thread alive
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\nShutting down honeypot...")

if __name__ == "__main__":
    main()