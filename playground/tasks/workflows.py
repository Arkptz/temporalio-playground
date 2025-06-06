from datetime import timedelta

from temporalio import workflow

from .shared import EchoActivityInput, EchoWorkflowInput


@workflow.defn(name="EchoWorkflow")
class EchoWorkflow:
    @workflow.run
    async def run(self, data: EchoWorkflowInput):
        data = EchoWorkflowInput.model_validate(data)
        for _ in range(data.count):
            await workflow.execute_activity(
                "echo",
                EchoActivityInput(message=data.message),
                start_to_close_timeout=timedelta(seconds=10),
            )
