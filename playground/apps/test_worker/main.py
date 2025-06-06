import asyncio
import logging

from infra.utils import circular_container_wire_and_init

from .container import AppContainer
from .settings import WIRE_MODULES

log = logging.getLogger(__name__)


async def async_main() -> None:
    container = AppContainer()
    await circular_container_wire_and_init(container, wire_modules=WIRE_MODULES)
    worker = container.temporal_worker()  # type: ignore
    if asyncio.isfuture(worker):
        worker = await worker
    await worker.run()


def main() -> None:
    asyncio.run(async_main())
