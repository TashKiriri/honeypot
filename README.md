# honeypot
# Basic Honeypot

A simple, educational honeypot implementation designed for learning cybersecurity concepts and analyzing attacker behavior. Built specifically for Kali Linux but compatible with most Linux distributions.

## 🔍 What is a Honeypot?

A honeypot is a cybersecurity mechanism that creates a decoy system to attract and analyze malicious activity. This implementation simulates common network services to log and study attack patterns.

## ✨ Features

- **Multi-Service Simulation**: SSH, HTTP, and FTP services
- **Concurrent Handling**: Thread-based architecture for multiple connections
- **JSON Logging**: Structured logs with timestamps and client information
- **Configurable Ports**: Easy to modify service ports
- **Log Analysis Tools**: Built-in scripts for analyzing captured data
- **Lightweight**: Uses only Python standard library

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/basic-honeypot.git
cd basic-honeypot

# Run setup script
chmod +x install.sh
./install.sh

# Start the honeypot
python3 honeypot.py
```

### Default Ports
- SSH: 2222
- HTTP: 8080
- FTP: 2121

## 📊 Usage

### Running the Honeypot
```bash
# Basic usage
python3 honeypot.py

# Run in background
nohup python3 honeypot.py > /dev/null 2>&1 &
```

### Monitoring Logs
```bash
# Real-time log viewing
tail -f honeypot.log

# Analyze logs
python3 log_analyzer.py honeypot.log
```

### Testing the Honeypot
```bash
# Test SSH honeypot
telnet localhost 2222

# Test HTTP honeypot
curl http://localhost:8080

# Test FTP honeypot
ftp localhost 2121
```

## 📈 Log Analysis

The honeypot generates JSON-formatted logs containing:
- Timestamp
- Service type
- Client IP address
- Request data

Example log entry:
```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "service": "SSH",
  "client_ip": "192.168.1.100",
  "data": "SSH-2.0-OpenSSH_8.0"
}
```

## ⚙️ Configuration

### Changing Ports
Edit the `services` list in `honeypot.py`:
```python
services = [
    (2222, SSHHoneypot, "SSH"),
    (8080, HTTPHoneypot, "HTTP"),
    (2121, FTPHoneypot, "FTP")
]
```

### Custom Log File
Modify the logger initialization:
```python
logger = HoneypotLogger("custom_honeypot.log")
```

## 🛡️ Security Considerations

⚠️ **Important Security Warnings:**

- **Isolation**: Run only in controlled, isolated environments
- **Firewall**: Implement proper firewall rules
- **Monitoring**: Actively monitor system resources
- **Legal Compliance**: Ensure compliance with local laws
- **Network Segmentation**: Consider network isolation

### Recommended Setup
```bash
# Create dedicated user
sudo useradd -r -s /bin/false honeypot

# Run in container (Docker example)
docker run -d --name honeypot -p 2222:2222 -p 8080:8080 -p 2121:2121 honeypot:latest
```

## 🔧 Advanced Features

### Adding Custom Services
```python
class CustomServiceHoneypot(BaseRequestHandler):
    def handle(self):
        logger = HoneypotLogger()
        client_ip = self.client_address[0]
        # Your service logic here
```

### Systemd Service
```bash
# Copy service file
sudo cp honeypot.service /etc/systemd/system/

# Enable and start
sudo systemctl enable honeypot
sudo systemctl start honeypot
```

## 📝 Log Analysis Examples

### Top Attacking IPs
```bash
grep -o '"client_ip":"[^"]*"' honeypot.log | sort | uniq -c | sort -nr | head -10
```

### Service Attack Distribution
```bash
grep -o '"service":"[^"]*"' honeypot.log | sort | uniq -c
```

### Hourly Attack Patterns
```bash
python3 log_analyzer.py honeypot.log
```

## 🤝 Contributing

Contributions are welcome! Please consider:

1. **Bug Reports**: Submit detailed issue reports
2. **Feature Requests**: Suggest new honeypot services
3. **Code Improvements**: Enhance existing functionality
4. **Documentation**: Improve setup and usage guides

### Development Setup
```bash
# Fork and clone
git clone https://github.com/yourusername/basic-honeypot.git

# Create feature branch
git checkout -b feature/new-service

# Make changes and test
python3 honeypot.py

# Submit pull request
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Notice

This software is intended for:
- Educational purposes
- Authorized security research
- Legitimate security testing

**Users are responsible for:**
- Compliance with local laws and regulations
- Obtaining proper authorization before deployment
- Responsible disclosure of any findings

## 🆘 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
sudo netstat -tulpn | grep :2222
sudo kill -9 <PID>
```

**Permission Denied**
- Use ports > 1024 for non-root execution
- Or run with `sudo` for standard ports

**No Incoming Connections**
- Check firewall settings: `sudo ufw status`
- Verify listening ports: `netstat -an | grep LISTEN`
- Test locally first: `telnet localhost 2222`

### Getting Help

1. Check the [Issues](https://github.com/yourusername/basic-honeypot/issues) page
2. Review the troubleshooting section
3. Submit a detailed bug report

## 📚 Resources

- [Honeypot Concepts](https://en.wikipedia.org/wiki/Honeypot_(computing))
- [Network Security Fundamentals](https://www.sans.org/white-papers/)
- [Python Socket Programming](https://docs.python.org/3/library/socket.html)

---

**⭐ If you find this project useful, please give it a star!**
