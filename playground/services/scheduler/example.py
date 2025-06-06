"""Example usage of SchedulerService

This example demonstrates how to use SchedulerService to launch
multiple EchoWorkflows with concurrency control and rate monitoring.
"""

import asyncio
import logging

from .container import SchedulerContainer

logging.basicConfig(level=logging.INFO)


async def batch_example():
    """Example of using SchedulerService for batch processing"""
    # Create container
    container = SchedulerContainer()

    # Create scheduler service with dependencies
    scheduler_service = container.scheduler_service(
        task_queue="benchmark",
        namespace="default",
        concurrency=5,
        report_interval=10,
    )

    # Run scheduler to launch specific number of workflows
    await scheduler_service.run(total_workflows=50, message="Batch test")


async def infinite_example():
    """Example of using SchedulerService for infinite processing"""
    # Create container
    container = SchedulerContainer()

    # Create scheduler service with dependencies
    scheduler_service = container.scheduler_service(
        task_queue="benchmark",
        namespace="default",
        concurrency=10,
        report_interval=5,  # Report every 5 seconds
    )

    print("Starting infinite scheduler. Press Ctrl+C to stop.")
    print("Statistics will be printed every 5 seconds.")

    try:
        # Run scheduler infinitely (like Go version)
        await scheduler_service.run_infinite(
            message="Infinite test",
            count=1,
            max_runtime=60,  # Run for 60 seconds max (remove for truly infinite)
        )
    except KeyboardInterrupt:
        print("Scheduler stopped by user")


async def main():
    """Choose which example to run"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "infinite":
        await infinite_example()
    else:
        await batch_example()


if __name__ == "__main__":
    asyncio.run(main())
