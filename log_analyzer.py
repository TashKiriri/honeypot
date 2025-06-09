#!/usr/bin/env python3
"""
Basic log analyzer for honeypot logs
"""
import json
import sys
from collections import defaultdict, Counter
from datetime import datetime

def analyze_logs(log_file):
    attempts = []
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    attempts.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"Log file {log_file} not found!")
        return
    
    if not attempts:
        print("No log entries found!")
        return
    
    print(f"Total attempts: {len(attempts)}")
    print("-" * 40)
    
    # Analyze by service
    services = Counter(attempt['service'] for attempt in attempts)
    print("Attempts by service:")
    for service, count in services.items():
        print(f"  {service}: {count}")
    
    print()
    
    # Analyze by IP
    ips = Counter(attempt['client_ip'] for attempt in attempts)
    print("Top 10 attacking IPs:")
    for ip, count in ips.most_common(10):
        print(f"  {ip}: {count} attempts")
    
    print()
    
    # Time analysis
    hours = Counter()
    for attempt in attempts:
        try:
            dt = datetime.fromisoformat(attempt['timestamp'])
            hours[dt.hour] += 1
        except:
            continue
    
    print("Attempts by hour:")
    for hour in sorted(hours.keys()):
        print(f"  {hour:02d}:00 - {hours[hour]} attempts")

if __name__ == "__main__":
    log_file = sys.argv[1] if len(sys.argv) > 1 else "honeypot.log"
    analyze_logs(log_file)