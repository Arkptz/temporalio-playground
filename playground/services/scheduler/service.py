import asyncio
import logging
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infra.temporalio_utils.service import TemporalService

log = logging.getLogger(__name__)


class SchedulerService:
    def __init__(
        self,
        temporal_service: "TemporalService",
        task_queue: str,
        namespace: str,
        concurrency: int = 10,
        report_interval: int = 10,
    ) -> None:
        self._temporal_service = temporal_service
        self._task_queue = task_queue
        self._namespace = namespace
        self._concurrency = concurrency
        self._report_interval = report_interval

        # Statistics
        self._total_workflows = 0
        self._last_completed = 0
        self._last_check = time.time()
        self._start_time = time.time()
        self._running_tasks = 0

        # Control
        self._semaphore = asyncio.Semaphore(concurrency)
        self._should_stop = False

    async def _start_single_workflow(self, message: str, count: int = 1) -> None:
        """Start a single workflow with semaphore control"""
        async with self._semaphore:
            self._running_tasks += 1
            try:
                workflow_id = await self._temporal_service.execute_echo_workflow(
                    namespace=self._namespace,
                    task_queue=self._task_queue,
                    message=message,
                    count=count,
                )
                self._total_workflows += 1
                log.debug(f"Started workflow: {workflow_id}")

            except Exception as e:
                log.error(f"Error starting workflow: {e}")
            finally:
                self._running_tasks -= 1

    async def _workflow_starter_loop(self, message: str, count: int = 1) -> None:
        """Infinite loop that starts workflows"""
        workflow_counter = 1

        while not self._should_stop:
            try:
                # Create task for starting workflow (non-blocking)
                asyncio.create_task(
                    self._start_single_workflow(
                        f"{message} #{workflow_counter}",
                        count,
                    ),
                )
                workflow_counter += 1

                # Small delay to prevent overwhelming
                await asyncio.sleep(0.01)

            except Exception as e:
                log.error(f"Error in workflow starter loop: {e}")
                await asyncio.sleep(1)

    async def _stats_reporter_loop(self) -> None:
        """Infinite loop that reports statistics every interval"""
        while not self._should_stop:
            await asyncio.sleep(self._report_interval)

            current_time = time.time()
            time_diff = current_time - self._last_check
            completed_diff = self._total_workflows - self._last_completed

            rate = completed_diff / time_diff if time_diff > 0 else 0

            # Report statistics similar to Go version
            log.info(
                f"Concurrent: {self._running_tasks} Workflows: {self._total_workflows} Rate: {rate:.2f}",
            )

            self._last_check = current_time
            self._last_completed = self._total_workflows

    async def run_infinite(
        self,
        message: str = "Scheduler test",
        count: int = 1,
        max_runtime: int | None = None,
    ) -> None:
        """Run scheduler infinitely, starting workflows continuously

        Args:
            message: Base message for workflows
            count: Count parameter for EchoWorkflow
            max_runtime: Optional maximum runtime in seconds (None for infinite)

        """
        log.info(
            f"Starting infinite scheduler: "
            f"concurrency: {self._concurrency}, "
            f"queue: {self._task_queue}, "
            f"namespace: {self._namespace}, "
            f"report_interval: {self._report_interval}s",
        )

        self._start_time = time.time()
        self._last_check = self._start_time

        try:
            # Start background tasks
            starter_task = asyncio.create_task(
                self._workflow_starter_loop(message, count),
            )
            reporter_task = asyncio.create_task(self._stats_reporter_loop())

            if max_runtime:
                # Run for specified time
                await asyncio.sleep(max_runtime)
            else:
                # Run indefinitely until interrupted
                await asyncio.gather(starter_task, reporter_task)

        except KeyboardInterrupt:
            log.info("Received interrupt signal, stopping scheduler...")
        finally:
            self._should_stop = True

            # Cancel background tasks
            if "starter_task" in locals():
                starter_task.cancel()
            if "reporter_task" in locals():
                reporter_task.cancel()

            # Wait for running workflows to complete
            log.info(
                f"Waiting for {self._running_tasks} running workflows to complete...",
            )
            while self._running_tasks > 0:
                await asyncio.sleep(0.1)

            # Final statistics
            total_time = time.time() - self._start_time
            final_rate = self._total_workflows / total_time if total_time > 0 else 0

            log.info(
                f"Scheduler stopped. Total workflows: {self._total_workflows}, "
                f"Runtime: {total_time:.2f}s, Average rate: {final_rate:.2f} wf/s",
            )

    async def run(
        self,
        total_workflows: int = 100,
        message: str = "Scheduler test",
    ) -> None:
        """Legacy method for backward compatibility - runs for specific number of workflows"""
        log.info(
            f"Starting batch scheduler: {total_workflows} workflows, "
            f"concurrency: {self._concurrency}, "
            f"queue: {self._task_queue}, "
            f"namespace: {self._namespace}",
        )

        self._start_time = time.time()

        # Create and run all tasks
        tasks = [
            self._start_single_workflow(f"{message} #{i}", 1)
            for i in range(1, total_workflows + 1)
        ]

        await asyncio.gather(*tasks, return_exceptions=True)

        # Final statistics
        elapsed_time = time.time() - self._start_time
        final_rate = self._total_workflows / elapsed_time if elapsed_time > 0 else 0

        log.info(
            f"Batch scheduler completed. Launched {self._total_workflows} workflows "
            f"in {elapsed_time:.2f}s, final rate: {final_rate:.2f} wf/s",
        )
