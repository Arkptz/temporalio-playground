import uuid

from tasks.shared import EchoWorkflowInput
from temporalio.client import Client


class TemporalService:
    def __init__(
        self,
        temporal_clients: dict[str, Client],
    ) -> None:
        self._temporal_clients = temporal_clients

    async def _terminate(self, namespace: str, workflow_id: str):
        try:
            await (
                self._temporal_clients[namespace]
                .get_workflow_handle(
                    workflow_id,
                )
                .terminate()
            )
        except:  # noqa
            pass

    async def execute_echo_workflow(
        self,
        namespace: str,
        task_queue: str,
        message: str = "Hello World",
        count: int = 1,
    ) -> str:
        """Starts EchoWorkflow and returns workflow_id"""
        workflow_id = f"echo-workflow-{uuid.uuid4()}"
        workflow_input = EchoWorkflowInput(message=message, count=count)

        await self._temporal_clients[namespace].execute_workflow(
            "EchoWorkflow",
            workflow_input,
            id=workflow_id,
            task_queue=task_queue,
        )

        return workflow_id
