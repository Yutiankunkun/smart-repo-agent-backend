from pydantic import BaseModel
from typing import Optional


class ApiResponse(BaseModel):
    """
    Entrypoint for the agent.
    """

    message: str
    error: Optional[str] = None

