# Temporal Load Testing Playground

A comprehensive testing environment for Temporal high-load scenarios with multiple backend configurations, monitoring, and benchmarking tools.

## 🎯 Project Overview

This repository provides a complete testing platform for evaluating Temporal performance under high-load conditions. It includes multiple infrastructure configurations, monitoring solutions, and custom Python benchmark tools to simulate real-world scenarios.

### Key Features

- **Multiple Backend Configurations**: MySQL + Elasticsearch, Cassandra + Elasticsearch
- **Comprehensive Monitoring**: Prometheus, Grafana, Node Exporter, Database metrics
- **Benchmark Tools**: Python scheduler service with infinite/batch modes
- **Production-ready Setup**: Multi-replica Temporal services with load balancing
- **Custom Workers**: Python workers with configurable concurrency

## 🏗️ Architecture Components

### Core Infrastructure

- **Temporal Server**: Multi-service architecture (frontend, history, matching, worker)
- **Databases**: MySQL 8.0 or Cassandra 3.x for persistence
- **Search**: Elasticsearch 7.x for advanced visibility
- **Monitoring**: Prometheus + Grafana stack with custom dashboards

### Benchmark Components

- **SchedulerService**: Python service for load generation
- **EchoWorkflow**: Simple workflow for testing throughput
- **Benchmark Workers**: Official Temporal benchmark workers

## 📁 Repository Structure

```
temporalio-playground/
├── compose/                          # Docker Compose configurations
│   ├── docker-compose-mysql-es.yaml      # MySQL + Elasticsearch setup
│   ├── docker-compose-cass-es.yaml       # Cassandra + Elasticsearch setup
│   ├── docker-compose-mysql-es-py-worker.yaml  # MySQL + Python workers
│   ├── config_sql.yaml                   # SQL backend configuration
│   ├── config_cassandra.yaml             # Cassandra backend configuration
│   ├── dynamicconfig/                    # Temporal dynamic configuration
│   ├── monitoring/                       # Monitoring configurations
│   └── MONITORING.md                     # Monitoring documentation
├── playground/                       # Python benchmark application
│   ├── services/scheduler/               # Scheduler service package
│   ├── apps/test_sheduler/              # Scheduler application
│   ├── apps/test_worker/                # Temporal worker application
│   ├── tasks/                           # Temporal workflows and activities
│   └── infra/                           # Infrastructure utilities
├── README.md                        # This file
├── README_SCHEDULER.md              # Scheduler service documentation
└── README_TEST_WORKER.md            # Test worker documentation
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- At least 8GB RAM available for containers
- 10GB free disk space

### 1. Choose Your Backend Configuration

#### Option A: MySQL + Elasticsearch (Recommended for testing)

```bash
cd compose
docker-compose -f docker-compose-mysql-es.yaml up -d
```

#### Option B: Cassandra + Elasticsearch (Production-like)

```bash
cd compose
docker-compose -f docker-compose-cass-es.yaml up -d
```

#### Option C: MySQL + Python Workers

```bash
cd compose
docker-compose -f docker-compose-mysql-es-py-worker.yaml up -d
```

### 2. Verify Services

```bash
# Check all services are running
docker-compose ps

# Wait for Temporal to be ready (may take 2-3 minutes)
curl -s http://localhost:8085/health
```

### 3. Access Interfaces

- **Temporal UI**: http://localhost:8085
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

## 📊 Docker Compose Configurations

### docker-compose-mysql-es.yaml

**Purpose**: Standard testing setup with MySQL backend

**Components**:

- MySQL 8.0 with optimized configuration
- Elasticsearch 7.x for visibility
- 5 replicas each of Temporal services (history, matching, worker, frontend)
- 15 benchmark workers for load generation
- Full monitoring stack (Prometheus, Grafana, exporters)

**Use Case**: General load testing, development, CI/CD

**Resource Requirements**: ~6GB RAM, 4 CPU cores

**Startup Command**:

```bash
docker-compose -f docker-compose-mysql-es.yaml up -d
```

### docker-compose-cass-es.yaml

**Purpose**: Production-like setup with Cassandra backend

**Components**:

- Cassandra 3.x cluster (6 nodes) with configurable replication
- Elasticsearch 7.x for visibility
- 1 replica each of Temporal services (lighter footprint)
- 15 benchmark workers
- Full monitoring stack

**Use Case**: Production testing, high-availability scenarios

**Resource Requirements**: ~8GB RAM, 6 CPU cores

**Startup Command**:

```bash
docker-compose -f docker-compose-cass-es.yaml up -d
```

### docker-compose-mysql-es-py-worker.yaml

**Purpose**: Custom Python worker testing

**Components**:

- MySQL 8.0 backend
- Elasticsearch 7.x
- 5 replicas of Temporal services
- Custom Python workers (from this repository)
- Monitoring stack

**Use Case**: Testing custom Python workflows, scheduler service validation

**Resource Requirements**: ~5GB RAM, 4 CPU cores

**Startup Command**:

```bash
docker-compose -f docker-compose-mysql-es-py-worker.yaml up -d
```

## 🔧 Configuration Files

### Database Configurations

- `config_sql.yaml`: MySQL backend configuration with optimized connection pools
- `config_cassandra.yaml`: Cassandra backend with multi-datacenter support

### Dynamic Configuration

- `dynamicconfig/dynamic_config_sql.yaml`: Runtime settings for SQL backend
- `dynamicconfig/dynamic_config_cass.yaml`: Runtime settings for Cassandra backend

### Key Settings

```yaml
# Workflow task processing
worker.persistenceMaxQPS: 5000
worker.ESProcessorNumOfWorkers: 10
history.persistenceMaxQPS: 3000

# Visibility processing
worker.ESProcessorBulkActions: 2500
history.visibilityProcessorMaxPollRPS: 3000
```

## 📈 Monitoring and Observability

### Monitoring Stack

- **Prometheus**: Metrics collection from all services
- **Grafana**: Pre-configured dashboards for Temporal and infrastructure
- **Node Exporter**: System metrics
- **MySQL/Elasticsearch Exporters**: Database-specific metrics

### Key Dashboards

1. **Temporal Server Metrics**: Request rates, latencies, queue depths
1. **SDK Metrics**: Client-side workflow and activity metrics
1. **Infrastructure Overview**: CPU, memory, disk, network
1. **Database Performance**: Query performance, connection pools, replication lag

### Accessing Monitoring

```bash
# Grafana (pre-configured dashboards)
open http://localhost:3001

# Prometheus (raw metrics)
open http://localhost:9090

# Temporal UI (workflow monitoring)
open http://localhost:8085
```

## 🏋️ Load Testing

### Built-in Benchmark Workers

Each compose file includes official Temporal benchmark workers that automatically generate load:

```yaml
benchmark-workers:
  image: ghcr.io/temporalio/benchmark-workers:latest
  environment:
    TEMPORAL_GRPC_ENDPOINT: "temporalio-frontend:7233"
    TEMPORAL_NAMESPACE: "default"
    TEMPORAL_TASK_QUEUE: "benchmark"
    TEMPORAL_WORKFLOW_TASK_POLLERS: "32"
    TEMPORAL_ACTIVITY_TASK_POLLERS: "32"
```

### Custom Python Scheduler

Use the custom scheduler service for controlled load testing:

```bash
# Infinite mode (like Go benchmark)
SCHEDULER_INFINITE_MODE=true \
SCHEDULER_CONCURRENCY=50 \
SCHEDULER_REPORT_INTERVAL=5 \
python -m playground.apps.test_sheduler.main

# Batch mode
SCHEDULER_INFINITE_MODE=false \
SCHEDULER_TOTAL_WORKFLOWS=1000 \
SCHEDULER_CONCURRENCY=20 \
python -m playground.apps.test_sheduler.main
```

### Load Testing Scenarios

#### Scenario 1: Basic Throughput Test

- **Target**: 1000+ workflows/second
- **Configuration**: docker-compose-mysql-es.yaml
- **Workers**: 15 benchmark workers + custom scheduler
- **Duration**: 10 minutes

#### Scenario 2: High Concurrency Test

- **Target**: 10,000 concurrent workflows
- **Configuration**: docker-compose-cass-es.yaml
- **Workers**: Custom scheduler with high concurrency
- **Monitoring**: Watch queue depths and latencies

#### Scenario 3: Endurance Test

- **Target**: Sustained load for 24+ hours
- **Configuration**: docker-compose-mysql-es.yaml
- **Workers**: Mixed benchmark + custom workers
- **Focus**: Memory leaks, performance degradation

## 🔍 Troubleshooting

### Common Issues

#### Services Won't Start

```bash
# Check logs
docker-compose logs temporalio-frontend

# Verify database connectivity
docker-compose logs mysql
docker-compose logs elasticsearch
```

#### High Memory Usage

```bash
# Monitor resource usage
docker stats

# Reduce replica counts in compose file
# Scale down services:
docker-compose scale temporalio-history=2
```

#### Slow Workflow Processing

```bash
# Check queue depths in Grafana
# Increase worker counts:
docker-compose scale benchmark-workers=20

# Tune dynamic configuration
# Edit dynamicconfig/dynamic_config_*.yaml
```

### Performance Tuning

#### Database Optimization

```yaml
# MySQL (my.cnf)
innodb_buffer_pool_size = 2G
max_connections = 1000

# Cassandra
MAX_HEAP_SIZE=2G
HEAP_NEWSIZE=400M
```

#### Temporal Tuning

```yaml
# Increase QPS limits
history.persistenceMaxQPS: 5000
matching.persistenceMaxQPS: 3000

# Optimize batch sizes
worker.ESProcessorBulkActions: 5000
```

## 🧪 Development Workflow

### Adding New Tests

1. Create new workflow/activity in `playground/tasks/`
1. Add test configuration in `playground/apps/`
1. Update scheduler service if needed
1. Run with existing Docker Compose setup

### Custom Compose Files

```bash
# Create custom configuration
cp docker-compose-mysql-es.yaml docker-compose-custom.yaml

# Modify settings for your test case
# Run with custom config
docker-compose -f docker-compose-custom.yaml up -d
```

## 📚 Documentation

- [Scheduler Service Documentation](README_SCHEDULER.md)
- [Test Worker Documentation](README_TEST_WORKER.md)
- [Monitoring Guide](compose/MONITORING.md)
- [Scheduler Package](playground/services/scheduler/README.md)

## 🤝 Contributing

1. Fork the repository
1. Create a feature branch
1. Add your test scenarios or improvements
1. Update documentation
1. Submit a pull request

## 📄 License

This project is provided as-is for testing and educational purposes.
