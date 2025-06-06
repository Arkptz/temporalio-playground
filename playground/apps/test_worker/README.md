# Test Worker Application

High-performance Temporal worker for processing EchoWorkflow tasks with automatic resource tuning.

## 🚀 Quick Start

```bash
# Set environment variables
export TEMPORAL_WORKER_NAMESPACE="default"
export TEMPORAL_WORKER_TASK_QUEUE="benchmark"
export DEFAULT_TEMPORAL_URL="localhost:7233"

# Run the worker
python -m playground.apps.test_worker.main
```

## 📁 Files

- `main.py` - Application entry point and worker startup
- `settings.py` - Configuration management with environment variables
- `container.py` - Dependency injection container setup

## 🔧 Key Features

- **Resource-Based Auto-Tuning**: Automatically adjusts concurrency based on CPU/memory usage
- **EchoWorkflow Processing**: Handles echo workflows for load testing
- **Docker Ready**: Optimized for containerized deployment
- **High Performance**: Configured for maximum throughput

## 📚 Full Documentation

For complete usage instructions, configuration options, and deployment guides, see:
[Test Worker Documentation](../../../README_TEST_WORKER.md)

## 🔗 Related Components

- **Scheduler Service**: Generates workflows that this worker processes
- **EchoWorkflow**: The workflow type handled by this worker
- **Docker Compose**: Orchestration with `docker-compose-mysql-es-py-worker.yaml`
