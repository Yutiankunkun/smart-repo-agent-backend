from pydantic import BaseModel,Field
from typing import Optional


class ChatInput(BaseModel):
    """
    You put the message here without any ids.
    """

    message: str = Field(
        description="message you put in the frame",
        examples=["Tell me about the information of the student sid0001."]
    )

class ToolExecution(BaseModel):
    """
    Agent can execute tools.
    """

    tool: str = Field(
        description="tool name",
    )

    input: str = Field(
        description="llm can input to get the tool",
    )

    output: str = Field(
        description="result of the tool",
    )


class ChatResponse(BaseModel):
    """
    Chat will return the response here.
    """

    reply: Optional[str] = Field(
        default=None,
        description="response from the agent",
    )

    tool_calls: list[str] = Field(
        default=[],
        description="name of the tools that agent called",
    )

    tool_executions: list[ToolExecution] = Field(
        default=[],
        description="tell you what the tool did",
    )

    error: Optional[str] = Field(
        default=None,
        description="error message",
    )