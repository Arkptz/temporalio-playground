import logging

from temporalio import activity

from .shared import EchoActivityInput

log = logging.getLogger(__name__)


@activity.defn(name="echo")
async def echo(data: EchoActivityInput):
    data = EchoActivityInput.model_validate(data)
    log.info(f"Echoing {data.message}")
