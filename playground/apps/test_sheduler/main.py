import asyncio
import logging
import signal
import sys

from infra.utils import circular_container_wire_and_init

from .container import AppContainer
from .settings import WIRE_MODULES

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


async def async_main() -> None:
    container = AppContainer()
    await circular_container_wire_and_init(container, wire_modules=WIRE_MODULES)

    # Get settings and create scheduler service
    settings = container.app_settings()
    log.info(f"Settings: {settings}")
    scheduler_service = container.scheduler_container.scheduler_service()
    if asyncio.isfuture(scheduler_service):
        scheduler_service = await scheduler_service

    if settings.scheduler_infinite_mode:
        log.info("Starting infinite scheduler service demonstration")

        # Setup signal handler for graceful shutdown
        def signal_handler(signum, frame):
            log.info(f"Received signal {signum}, stopping scheduler...")
            scheduler_service._should_stop = True

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        try:
            # Run scheduler infinitely
            max_runtime = (
                settings.scheduler_max_runtime
                if settings.scheduler_max_runtime > 0
                else None
            )
            await scheduler_service.run_infinite(
                message=settings.scheduler_message,
                count=3,
                max_runtime=max_runtime,
            )
        except KeyboardInterrupt:
            log.info("Keyboard interrupt received")
    else:
        log.info("Starting batch scheduler service demonstration")

        # Run scheduler for specific number of workflows
        await scheduler_service.run(
            total_workflows=settings.scheduler_total_workflows,
            message=settings.scheduler_message,
        )

    log.info("Demonstration completed")


def main() -> None:
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        log.info("Application interrupted")
        sys.exit(0)
