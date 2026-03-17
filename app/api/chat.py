import json
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.agent.agent import run_agent
from app.core.database import get_db
from app.schemas.chat import ChatResponse, ChatInput


router = APIRouter()

@router.post(
    "/",
    response_model=ChatResponse,
    summary="Chat Api",
)
def chat(
        data: ChatInput,
        db: Session = Depends(get_db),
):
    """
    User input message -> loop -> executor -> agent output message.
    Agent can think and pick the right tool and decide what to do.

    :param db:
    :param data:
    :return:
    """

    result = run_agent(
        user_message=data.message,
        db=db,
    )
    return ChatResponse(
        reply=result.get("reply"),
        tool_calls=result.get("tools_used", []),
        tool_executions=[
            {"tool": t["tool"], "input": json.dumps(t["input"], ensure_ascii=False), "output": t["output"]}
            for t in result.get("tools_result", [])
        ],
        error=result.get("error"),
    )

