from pydantic import BaseModel


class EchoActivityInput(BaseModel):
    message: str


class EchoWorkflowInput(BaseModel):
    message: str
    count: int
