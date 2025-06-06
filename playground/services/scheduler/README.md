# Scheduler Package

Modular scheduler service package for launching Temporal workflows with concurrency control and performance monitoring.

## Package Structure

```
playground/services/scheduler/
├── __init__.py          # Package exports
├── service.py           # SchedulerService implementation
├── container.py         # Dependency injection container
├── example.py           # Usage examples
└── README.md           # This file
```

## Modules

### service.py

Contains the main `SchedulerService` class with two execution modes:

- **Batch Mode**: launches specific number of workflows and stops
- **Infinite Mode**: continuously launches workflows until stopped (Go-like behavior)

### container.py

Contains `SchedulerContainer` with dependency injection setup for:

- TemporalService integration
- Configurable parameters (task_queue, namespace, concurrency, report_interval)

### example.py

Provides usage examples for both batch and infinite modes.

## Usage

### Import

```python
from services.scheduler import SchedulerService, SchedulerContainer
```

### Basic Usage

```python
# Create container
container = SchedulerContainer()

# Create service
scheduler_service = container.scheduler_service(
    task_queue="benchmark",
    namespace="default",
    concurrency=10,
    report_interval=10
)

# Run infinite mode (Go-like)
await scheduler_service.run_infinite(
    message="Load test",
    max_runtime=None  # None = infinite
)
```

## Design Principles

- **Modularity**: Self-contained package with clear interfaces
- **Dependency Injection**: All dependencies injected through container
- **Type Safety**: Full type annotations
- **Go Compatibility**: Infinite mode mimics Go benchmark tool behavior
- **Backward Compatibility**: Legacy batch mode preserved
