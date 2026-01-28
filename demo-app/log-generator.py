#!/usr/bin/env python3
import json
import time
import random
from datetime import datetime

# Các template log mô phỏng
LOG_TEMPLATES = [
    {"severity": "INFO", "message": "User login successful", "latency_ms": lambda: random.randint(50, 200)},
    {"severity": "INFO", "message": "API request processed", "latency_ms": lambda: random.randint(100, 500)},
    {"severity": "WARN", "message": "Slow database query", "latency_ms": lambda: random.randint(800, 1500)},
    {"severity": "ERROR", "message": "Database connection timeout", "latency_ms": lambda: random.randint(3000, 5000)},
    {"severity": "ERROR", "message": "External API call failed", "latency_ms": lambda: random.randint(2000, 4000)},
]

def generate_log():
    template = random.choice(LOG_TEMPLATES)
    
    # Tạo log theo chuẩn OpenTelemetry
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "severity": template["severity"],
        "body": template["message"],
        "attributes": {
            "http.method": random.choice(["GET", "POST", "PUT"]),
            "http.url": f"/api/v1/{random.choice(['users', 'orders', 'products'])}",
            "http.status_code": random.choice([200, 200, 200, 400, 500]),
            "user.id": f"user_{random.randint(1000, 9999)}",
            "latency_ms": template["latency_ms"]()
        },
        "resource": {
            "service.name": "demo-service",
            "service.version": "1.0.0",
            "host.name": "demo-server-01"
        },
        "traceId": f"trace_{random.randint(100000, 999999)}",
        "spanId": f"span_{random.randint(1000, 9999)}"
    }
    
    return log_entry

if __name__ == "__main__":
    print("Starting log generator...")
    while True:
        log = generate_log()
        print(json.dumps(log))
        
        # Random delay để mô phỏng traffic thực tế
        time.sleep(random.uniform(0.1, 2.0))
