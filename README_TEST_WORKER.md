# Test Worker Documentation

A configurable Temporal worker application for processing EchoWorkflow tasks with resource-based auto-tuning and high-performance settings.

## 🎯 Overview

The test-worker is a production-ready Temporal worker implementation that automatically processes workflows and activities. It features:

- **Resource-Based Auto-Tuning**: Automatically adjusts concurrency based on CPU and memory usage
- **EchoWorkflow Processing**: Handles EchoWorkflow tasks for load testing scenarios
- **High Performance Configuration**: Optimized for high-throughput processing
- **Docker Integration**: Ready for containerized deployment

## 📁 Project Structure

```
playground/apps/test_worker/
├── __init__.py          # Package initialization
├── main.py              # Application entry point
├── settings.py          # Configuration settings
└── container.py         # Dependency injection container
```

## 🔧 Architecture

### Components

1. **Main Application** (`main.py`): Entry point that starts the worker
1. **Settings** (`settings.py`): Configuration management with environment variable support
1. **Container** (`container.py`): Dependency injection setup for worker components
1. **Worker Configuration**: Resource-based tuning with automatic slot management

### Dependencies

- **EchoWorkflow**: Processes echo workflows from the tasks module
- **Echo Activity**: Executes echo activities
- **Temporal Client**: Connects to Temporal server
- **Resource-Based Tuner**: Automatically adjusts worker capacity

## ⚙️ Configuration

### Environment Variables

#### Required Settings

```bash
# Temporal Connection
TEMPORAL_WORKER_NAMESPACE="default"           # Temporal namespace to connect to
TEMPORAL_WORKER_TASK_QUEUE="benchmark"       # Task queue to process

# Basic Configuration
DEFAULT_TEMPORAL_URL="localhost:7233"         # Temporal server address
DEFAULT_TEMPORAL_NAMESPACE="default"          # Default namespace
```

#### Resource Tuning (Optional)

```bash
# CPU and Memory Targets
TEMPORAL_WORKER_TARGET_CPU=0.9                # Target CPU utilization (0.0-1.0)
TEMPORAL_WORKER_TARGET_RAM=0.8                # Target RAM utilization (0.0-1.0)

# Workflow Slot Configuration
TEMPORAL_WORKER_WORKFLOWS_MIN_SLOTS=10        # Minimum workflow slots
TEMPORAL_WORKER_WORKFLOWS_MAX_SLOTS=500       # Maximum workflow slots

# Activity Slot Configuration
TEMPORAL_WORKER_ACTIVITIES_MIN_SLOTS=50       # Minimum activity slots
TEMPORAL_WORKER_ACTIVITIES_MAX_SLOTS=500      # Maximum activity slots

# Local Activity Slot Configuration
TEMPORAL_WORKER_LOCAL_ACTIVITIES_MIN_SLOTS=50 # Minimum local activity slots
TEMPORAL_WORKER_LOCAL_ACTIVITIES_MAX_SLOTS=500 # Maximum local activity slots

# Polling Configuration
TEMPORAL_WORKER_MAX_CONCURRENT_WORKFLOW_TASK_POLLS=100  # Max concurrent workflow polls
TEMPORAL_WORKER_MAX_CONCURRENT_ACTIVITY_TASK_POLLS=100  # Max concurrent activity polls
TEMPORAL_WORKER_NONSTICKY_TO_STICKY_POLL_RATIO=0.5     # Non-sticky to sticky poll ratio
```

### Configuration Examples

#### High-Performance Setup

```bash
export TEMPORAL_WORKER_TARGET_CPU=0.9
export TEMPORAL_WORKER_TARGET_RAM=0.8
export TEMPORAL_WORKER_WORKFLOWS_MAX_SLOTS=1000
export TEMPORAL_WORKER_ACTIVITIES_MAX_SLOTS=2000
export TEMPORAL_WORKER_MAX_CONCURRENT_WORKFLOW_TASK_POLLS=200
export TEMPORAL_WORKER_MAX_CONCURRENT_ACTIVITY_TASK_POLLS=200
```

#### Conservative Setup

```bash
export TEMPORAL_WORKER_TARGET_CPU=0.6
export TEMPORAL_WORKER_TARGET_RAM=0.6
export TEMPORAL_WORKER_WORKFLOWS_MAX_SLOTS=100
export TEMPORAL_WORKER_ACTIVITIES_MAX_SLOTS=200
export TEMPORAL_WORKER_MAX_CONCURRENT_WORKFLOW_TASK_POLLS=50
export TEMPORAL_WORKER_MAX_CONCURRENT_ACTIVITY_TASK_POLLS=50
```

## 🚀 Usage

### Local Development

#### Direct Execution

```bash
# Set environment variables
export TEMPORAL_WORKER_NAMESPACE="default"
export TEMPORAL_WORKER_TASK_QUEUE="benchmark"
export DEFAULT_TEMPORAL_URL="localhost:7233"

# Run the worker
python -m playground.apps.test_worker.main
```

#### Using direnv (Recommended)

```bash
# Create .env file
cat > .env << EOF
TEMPORAL_WORKER_NAMESPACE=default
TEMPORAL_WORKER_TASK_QUEUE=benchmark
DEFAULT_TEMPORAL_URL=localhost:7233
TEMPORAL_WORKER_TARGET_CPU=0.9
TEMPORAL_WORKER_TARGET_RAM=0.8
EOF

# Load environment and run
direnv reload
python -m playground.apps.test_worker.main
```

### Docker Deployment

#### Standalone Container

```bash
# Build image
docker build -t test-worker --build-arg PROJECT_NAME=test-worker .

# Run container
docker run -d \
  --name test-worker \
  --network temporal-network \
  -e TEMPORAL_WORKER_NAMESPACE=default \
  -e TEMPORAL_WORKER_TASK_QUEUE=benchmark \
  -e DEFAULT_TEMPORAL_URL=temporalio-frontend:7233 \
  -e TEMPORAL_WORKER_TARGET_CPU=0.9 \
  -e TEMPORAL_WORKER_TARGET_RAM=0.8 \
  test-worker
```

#### Docker Compose Integration

The worker is already integrated in `docker-compose-mysql-es-py-worker.yaml`:

```yaml
test-worker:
  build:
    context: ../
    args:
      PROJECT_NAME: "test-worker"
  environment:
    DEFAULT_TEMPORAL_URL: "temporalio-frontend:7233"
    DEFAULT_TEMPORAL_NAMESPACE: "default"
    TEMPORAL_WORKER_NAMESPACE: "default"
    TEMPORAL_WORKER_TASK_QUEUE: "benchmark"
    TEMPORAL_WORKER_TARGET_CPU: "0.9"
    TEMPORAL_WORKER_TARGET_RAM: "0.8"
    # ... additional settings
  deploy:
    mode: replicated
    replicas: 10
```

### Scaling Workers

```bash
# Scale up workers in Docker Compose
docker-compose scale test-worker=20

# Or modify replicas in compose file
deploy:
  mode: replicated
  replicas: 50
```

## 📊 Resource-Based Auto-Tuning

### How It Works

The worker uses Temporal's ResourceBasedTuner to automatically adjust concurrency:

1. **Monitoring**: Continuously monitors CPU and memory usage
1. **Slot Adjustment**: Increases/decreases workflow and activity slots based on resource utilization
1. **Target-Based**: Maintains CPU and memory usage close to configured targets
1. **Boundaries**: Respects minimum and maximum slot limits

### Tuning Parameters

```python
# Resource targets (0.0 to 1.0)
target_cpu = 0.9    # 90% CPU utilization target
target_ram = 0.8    # 80% RAM utilization target

# Slot boundaries
workflow_slots: 10-500     # Min-Max workflow concurrency
activity_slots: 50-500     # Min-Max activity concurrency
local_activity_slots: 50-500  # Min-Max local activity concurrency
```

### Benefits

- **Automatic Scaling**: No manual tuning required
- **Resource Efficiency**: Maximizes throughput while preventing resource exhaustion
- **Adaptive**: Responds to changing workload patterns
- **Safe Boundaries**: Prevents overwhelming the system

## 🔍 Monitoring and Observability

### Logs

```bash
# View worker logs
docker-compose logs test-worker

# Follow logs in real-time
docker-compose logs -f test-worker

# Filter logs by level
docker-compose logs test-worker | grep ERROR
```

### Key Log Messages

- `Worker started`: Worker successfully connected to Temporal
- `Tuner adjusted slots`: Resource-based tuning in action
- `Task processed`: Successfully completed workflow/activity
- `Connection error`: Issues connecting to Temporal server

### Metrics Integration

The worker automatically exports metrics to Temporal server, which are then collected by Prometheus in the monitoring stack:

- **Worker Health**: Connection status, uptime
- **Task Processing**: Workflow/activity completion rates, latencies
- **Resource Usage**: CPU, memory, slot utilization
- **Error Rates**: Failed tasks, connection errors

View metrics in Grafana dashboards:

- Worker Service Dashboard
- SDK Metrics Dashboard

## 🧪 Testing and Validation

### Verify Worker Connection

```bash
# Check worker is registered in Temporal UI
open http://localhost:8085

# Navigate to: Workers -> Task Queue: benchmark
# Should see active workers listed
```

### Test EchoWorkflow Processing

```bash
# Use scheduler to send test workflows
SCHEDULER_TASK_QUEUE=benchmark \
SCHEDULER_CONCURRENCY=10 \
SCHEDULER_TOTAL_WORKFLOWS=100 \
python -m playground.apps.test_sheduler.main
```

### Performance Testing

```bash
# High-load test with multiple workers
docker-compose scale test-worker=20

# Monitor resource usage
docker stats

# Check processing rate in Grafana
open http://localhost:3001
```

## 🛠️ Troubleshooting

### Common Issues

#### Worker Won't Start

```bash
# Check environment variables
env | grep TEMPORAL

# Verify Temporal server connection
nc -zv localhost 7233

# Check container logs
docker-compose logs test-worker
```

#### High Memory Usage

```bash
# Reduce memory target
export TEMPORAL_WORKER_TARGET_RAM=0.6

# Reduce maximum slots
export TEMPORAL_WORKER_ACTIVITIES_MAX_SLOTS=200
export TEMPORAL_WORKER_WORKFLOWS_MAX_SLOTS=100

# Restart worker
docker-compose restart test-worker
```

#### Low Throughput

```bash
# Increase resource targets
export TEMPORAL_WORKER_TARGET_CPU=0.95
export TEMPORAL_WORKER_TARGET_RAM=0.9

# Increase maximum slots
export TEMPORAL_WORKER_ACTIVITIES_MAX_SLOTS=1000
export TEMPORAL_WORKER_WORKFLOWS_MAX_SLOTS=500

# Scale up workers
docker-compose scale test-worker=30
```

#### Connection Issues

```bash
# Check Temporal server status
curl -s http://localhost:8085/health

# Verify network connectivity
docker network inspect temporal-network

# Check DNS resolution
docker exec test-worker nslookup temporalio-frontend
```

### Performance Tuning Tips

1. **CPU-Bound Workloads**: Increase `TEMPORAL_WORKER_TARGET_CPU` to 0.95
1. **Memory-Bound Workloads**: Monitor memory usage and adjust `TEMPORAL_WORKER_TARGET_RAM`
1. **I/O-Bound Workloads**: Increase activity slots for better parallelism
1. **Mixed Workloads**: Use default settings and let auto-tuning optimize

## 📚 Related Documentation

- [Main README](README.md) - Complete project overview
- [Scheduler Documentation](README_SCHEDULER.md) - Load generation tools
- [Docker Compose Guide](compose/README.md) - Container orchestration
- [Monitoring Guide](compose/MONITORING.md) - Observability setup

## 🔗 Integration Points

### With Scheduler Service

- Processes workflows generated by `test_sheduler` application
- Shares same task queue (`benchmark` by default)
- Scales independently for optimal resource utilization

### With Docker Compose

- Included in `docker-compose-mysql-es-py-worker.yaml`
- Automatically connected to Temporal network
- Pre-configured with optimal settings

### With Monitoring

- Metrics automatically collected by Prometheus
- Performance dashboards available in Grafana
- Logs centrally managed through Docker logging driver
