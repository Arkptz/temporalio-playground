import logging

from dependency_injector import providers
from dependency_injector.containers import (
    DeclarativeContainer,
)  # pylint: disable=no-name-in-module

log = logging.getLogger(__name__)


async def circular_container_wire_and_init(
    container: DeclarativeContainer,
    wire_modules: list[str],
):
    log.info(f"start wiring wire_modules: {wire_modules}")
    container.wire(
        modules=wire_modules,
    )
    container.init_resources()
    # try:
    #     await awaitable  # type: ignore
    # except:
    #     pass
    dct = container.__dict__
    for key in dct:
        if key == "parent":
            continue
        value = dct[key]
        if isinstance(value, providers.Container):
            await circular_container_wire_and_init(value(), wire_modules)
