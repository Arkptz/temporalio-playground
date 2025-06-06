# SchedulerService

A scheduler service for launching Temporal workflows with concurrency control and performance monitoring. Supports both batch and infinite execution modes similar to the Go benchmark tool.

## Package Structure

The scheduler functionality is organized as a modular package:

```
playground/services/scheduler/
├── __init__.py          # Package exports
├── service.py           # SchedulerService implementation
├── container.py         # Dependency injection container
├── example.py           # Usage examples
└── README.md           # Package documentation
```

## Architecture

### SchedulerService

Main service for launching EchoWorkflows with concurrency limits compliance. Now supports two execution modes:

1. **Batch Mode** - launches a specific number of workflows and stops
1. **Infinite Mode** - continuously launches workflows until stopped (similar to Go version)

**Constructor parameters:**

- `temporal_service` - TemporalService instance for Temporal interaction
- `task_queue` - Temporal queue for workflow execution
- `namespace` - Temporal namespace
- `concurrency` - maximum number of simultaneously launched workflows
- `report_interval` - interval in seconds for statistics reporting (default: 10)

**Methods:**

- `run()` - batch mode: launches specific number of workflows
- `run_infinite()` - infinite mode: continuously launches workflows with periodic stats

### TemporalService

Added `start_echo_workflow` method for launching EchoWorkflow:

```python
async def start_echo_workflow(
    self,
    namespace: str,
    task_queue: str,
    message: str = "Hello World",
    count: int = 1
) -> str:
```

## Functionality

### Infinite Mode (Go-like behavior)

- Continuously starts workflows in background
- Reports statistics every N seconds: `Concurrent: X Workflows: Y Rate: Z.ZZ`
- Graceful shutdown on SIGINT/SIGTERM
- Configurable concurrency and reporting interval

### Batch Mode (Legacy)

- Launches specific number of workflows
- Reports final statistics
- Backward compatible with existing code

### Concurrency Control

Uses `asyncio.Semaphore` to limit the number of simultaneously executing workflow launch operations.

### Performance Monitoring

- Rate calculation (workflows per second)
- Real-time concurrent task tracking
- Periodic statistics reporting
- Final statistics upon completion

### Error Handling

Each workflow launches in a separate task with exception handling.

## Usage

### Import

```python
from services.scheduler import SchedulerService, SchedulerContainer
```

### Infinite Mode (Go-like)

```python
# Create scheduler service
scheduler_service = container.scheduler_container.scheduler_service(
    task_queue="benchmark",
    namespace="default",
    concurrency=10,
    report_interval=10
)

# Run infinitely
await scheduler_service.run_infinite(
    message="Load test",
    count=1,
    max_runtime=None  # None = infinite, or specify seconds
)
```

### Batch Mode

```python
# Run for specific number of workflows
await scheduler_service.run(
    total_workflows=100,
    message="Batch test"
)
```

### Through test_sheduler application

#### Infinite Mode

```bash
# Environment variables
SCHEDULER_INFINITE_MODE=true
SCHEDULER_CONCURRENCY=20
SCHEDULER_REPORT_INTERVAL=5
SCHEDULER_MAX_RUNTIME=0  # 0 = infinite

# Run
python -m playground.apps.test_sheduler.main
```

#### Batch Mode

```bash
# Environment variables
SCHEDULER_INFINITE_MODE=false
SCHEDULER_TOTAL_WORKFLOWS=500
SCHEDULER_CONCURRENCY=10

# Run
python -m playground.apps.test_sheduler.main
```

## Output Examples

### Infinite Mode Output

```
INFO:playground.apps.test_sheduler.main:Starting infinite scheduler service demonstration
INFO:playground.services.scheduler.service:Starting infinite scheduler: concurrency: 10, queue: benchmark, namespace: default, report_interval: 10s
Concurrent: 8 Workflows: 45 Rate: 4.50
Concurrent: 10 Workflows: 89 Rate: 4.40
Concurrent: 9 Workflows: 134 Rate: 4.50
^C
INFO:playground.services.scheduler.service:Received interrupt signal, stopping scheduler...
INFO:playground.services.scheduler.service:Waiting for 9 running workflows to complete...
INFO:playground.services.scheduler.service:Scheduler stopped. Total workflows: 142, Runtime: 32.45s, Average rate: 4.37 wf/s
```

### Batch Mode Output

```
INFO:playground.apps.test_sheduler.main:Starting batch scheduler service demonstration
INFO:playground.services.scheduler.service:Starting batch scheduler: 100 workflows, concurrency: 10, queue: benchmark, namespace: default
INFO:playground.services.scheduler.service:Batch scheduler completed. Launched 100 workflows in 4.23s, final rate: 23.64 wf/s
```

## Configuration

### Settings

```python
class Settings(BaseSettings):
    # Basic scheduler settings
    scheduler_task_queue: str = "benchmark"
    scheduler_namespace: str = "default"
    scheduler_concurrency: int = 10
    scheduler_message: str = "Test scheduler"

    # Batch mode settings
    scheduler_total_workflows: int = 100

    # Infinite mode settings
    scheduler_infinite_mode: bool = False
    scheduler_report_interval: int = 10  # seconds
    scheduler_max_runtime: int = 0  # 0 = infinite, >0 = max seconds
```

## Signal Handling

The infinite mode supports graceful shutdown:

- `SIGINT` (Ctrl+C) - stops scheduler and waits for running workflows
- `SIGTERM` - same as SIGINT
- Proper cleanup of background tasks
- Final statistics reporting

## Design Principles

1. **Go Compatibility** - infinite mode behaves like the Go benchmark tool
1. **Modularity** - organized as self-contained package with clear interfaces
1. **DRY** - reusing TemporalService and common containers
1. **Dependency Injection** - all dependencies passed through containers
1. **Type Safety** - full typing with TYPE_CHECKING usage
1. **Logging** - detailed logging for performance monitoring
1. **Error Handling** - graceful handling of exceptions during workflow launch
1. **Backward Compatibility** - legacy batch mode still supported
