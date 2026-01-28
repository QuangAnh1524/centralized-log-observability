# 🚀 Smart Log Lab

A **modern observability stack** for centralized log collection, processing, and visualization using **Kafka**, **Vector**, **Loki**, **MinIO**, and **Grafana**.

![Stack](https://img.shields.io/badge/Kafka-KRaft-orange?style=flat-square&logo=apachekafka)
![Stack](https://img.shields.io/badge/Loki-3.4.0-yellow?style=flat-square&logo=grafana)
![Stack](https://img.shields.io/badge/Vector-0.52.0-purple?style=flat-square)
![Stack](https://img.shields.io/badge/MinIO-S3-red?style=flat-square&logo=minio)

---

## 📋 Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Demo App      │     │  Vector Agent   │     │     Kafka       │
│ (Log Generator) │────▶│  (Collector)    │────▶│   (raw-logs)    │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Grafana      │◀────│      Loki       │◀────│Vector Aggregator│
│  (Dashboard)    │     │   (Storage)     │     │  (Processing)   │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │      MinIO      │
                        │  (S3 Storage)   │
                        └─────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| **Kafka** | 7.6.0 (KRaft) | Message broker for log streaming |
| **Vector** | 0.52.0 | Log collection & aggregation |
| **Loki** | 3.4.0 | Log storage & querying |
| **MinIO** | Latest | S3-compatible object storage |
| **Grafana** | Latest | Visualization & dashboards |

---

## 📥 Prerequisites

### Download Vector Binary

> ⚠️ **Note**: The Vector binary is not included in this repository due to GitHub's 100MB file size limit. You need to download it manually.

**Option 1: Download from official website**

```bash
# Linux/macOS
curl --proto '=https' --tlsv1.2 -sSfL https://sh.vector.dev | bash

# Or download specific version (0.52.0)
# Visit: https://vector.dev/releases/0.52.0/download/
```

**Option 2: Download and extract manually**

```bash
# Linux x86_64
wget https://packages.timber.io/vector/0.52.0/vector-0.52.0-x86_64-unknown-linux-gnu.tar.gz
tar -xzf vector-0.52.0-x86_64-unknown-linux-gnu.tar.gz
cp vector-0.52.0-x86_64-unknown-linux-gnu/bin/vector vector-agent/vector-deploy/bin/

# Windows
# Download from: https://packages.timber.io/vector/0.52.0/vector-0.52.0-x86_64-pc-windows-msvc.zip
```

**Option 3: Use Docker (recommended for production)**

```bash
docker pull timberio/vector:0.52.0-alpine
```

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/smart_log-lab.git
cd smart_log-lab
```

### 2. Setup Configuration

```bash
cd configs

# Copy example configs
cp loki-config.yml.example loki-config.yml
cp vector-agent.toml.example vector-agent.toml
cp vector-aggregator.toml.example vector-aggregator.toml

# Edit loki-config.yml with your MinIO credentials
```

### 3. Start Services

```bash
docker-compose -f docker-compose.kafka_minio_loki_aggregator.yml up -d
```

### 4. Create MinIO Bucket

1. Open MinIO Console: http://localhost:9001
2. Login with your credentials
3. Create bucket: `loki-chunks`

### 5. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| MinIO Console | http://localhost:9001 | Your config |
| Loki API | http://localhost:3100 | - |
| Kafka | localhost:9092 | - |

---

## 📁 Project Structure

```
smart_log-lab/
├── configs/                    # Configuration files
│   ├── loki-config.yml         # Loki configuration (git-ignored)
│   ├── loki-config.yml.example # Loki config template
│   ├── vector-agent.toml       # Vector Agent config (git-ignored)
│   ├── vector-agent.toml.example
│   ├── vector-aggregator.toml  # Vector Aggregator config (git-ignored)
│   └── vector-aggregator.toml.example
├── demo-app/
│   └── log-generator.py        # Demo log generator
├── docker-compose.kafka_minio_loki_aggregator.yml
├── grafana/                    # Grafana provisioning
├── kafka/                      # Kafka data (git-ignored)
├── loki/                       # Loki data (git-ignored)
├── minio/                      # MinIO data (git-ignored)
├── vector-agent/               # Vector agent files
├── vector-aggregator/          # Vector aggregator files
└── .gitignore
```

---

## 🔧 Configuration

### Loki Config (`configs/loki-config.yml`)

Key settings to configure:

```yaml
storage_config:
  aws:
    access_key_id: YOUR_MINIO_ACCESS_KEY
    secret_access_key: YOUR_MINIO_SECRET_KEY
```

### Vector Agent (`configs/vector-agent.toml`)

Collects logs from files and sends to Kafka:

```toml
[sources.demo_app_logs]
type = "file"
include = ["/var/log/demo/*.log"]

[sinks.to_kafka]
type = "kafka"
bootstrap_servers = "kafka:9092"
topic = "raw-logs"
```

### Vector Aggregator (`configs/vector-aggregator.toml`)

Consumes from Kafka, transforms, and sends to Loki:

```toml
[sources.from_kafka]
type = "kafka"
topics = ["raw-logs"]

[sinks.to_loki]
type = "loki"
endpoint = "http://loki:3100"
```

---

## 🧪 Demo Log Generator

Run the demo app to generate sample logs:

```bash
python demo-app/log-generator.py
```

Sample output (OpenTelemetry format):

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "severity": "INFO",
  "body": "User login successful",
  "attributes": {
    "http.method": "POST",
    "http.status_code": 200,
    "latency_ms": 150
  },
  "resource": {
    "service.name": "demo-service"
  },
  "traceId": "trace_123456"
}
```

---

## 📊 Features

- ✅ **Kafka KRaft Mode** - No Zookeeper required
- ✅ **S3-Compatible Storage** - MinIO for Loki chunks
- ✅ **Log-to-Metrics** - Convert logs to Prometheus metrics
- ✅ **OpenTelemetry Format** - Standard log format
- ✅ **31-Day Retention** - Configurable log retention
- ✅ **Health Checks** - Built-in container health monitoring

---

## 🔒 Security Notes

> ⚠️ **Important**: Never commit real credentials to Git!

- All config files with credentials are `.gitignore`d
- Use `.example` files as templates
- Store secrets in environment variables for production

---

## 📝 License

MIT License - feel free to use for learning and development.

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

**Made with ❤️ for Log Engineering Labs**
