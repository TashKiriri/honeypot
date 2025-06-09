#!/bin/bash
echo "Setting up Basic Honeypot..."

# Create logs directory
mkdir -p logs

# Make honeypot executable
chmod +x honeypot.py
chmod +x log_analyzer.py

# Check if ports are available
echo "Checking port availability..."
if netstat -tuln | grep -q ":2222 "; then
    echo "Warning: Port 2222 is already in use"
fi
if netstat -tuln | grep -q ":8080 "; then
    echo "Warning: Port 8080 is already in use"
fi
if netstat -tuln | grep -q ":2121 "; then
    echo "Warning: Port 2121 is already in use"
fi

# Test Python modules
echo "Testing Python dependencies..."
python3 -c "import socket, threading, datetime, json, os, socketserver" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ All Python modules available"
else
    echo "✗ Missing Python modules"
    exit 1
fi

# Create systemd service file (optional)
if [ "$EUID" -eq 0 ]; then
    cat > /etc/systemd/system/honeypot.service << EOF
[Unit]
Description=Basic Honeypot Service
After=network.target

[Service]
Type=simple
User=nobody
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/honeypot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    echo "✓ Systemd service file created"
    echo "  Enable with: sudo systemctl enable honeypot"
    echo "  Start with: sudo systemctl start honeypot"
else
    echo "Run as root to create systemd service"
fi

echo ""
echo "Setup complete!"
echo "Usage:"
echo "  Start honeypot: python3 honeypot.py"
echo "  View logs: tail -f honeypot.log"
echo "  Analyze logs: python3 log_analyzer.py"
echo ""
echo "Test connections:"
echo "  SSH: telnet localhost 2222"
echo "  HTTP: curl http://localhost:8080"
echo "  FTP: ftp localhost 2121"