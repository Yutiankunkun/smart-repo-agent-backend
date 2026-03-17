import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from app.agent.executor import execute_tool
from app.agent.tools import TOOLS
from sqlalchemy.orm import Session


load_dotenv()

MAX_ITERATIONS = 5
MAX_TOKENS = 1000

AGENT_SYSTEM_PROMPT = """You are an academic assistant at a private tutoring school. Your role is to help the homeroom teacher with their tasks.

You have access to multiple tools. Understand the homeroom teacher’s message, choose the appropriate tools, and execute them.

Rules:
1. When the homeroom teacher sends an interview/meeting memo, first determine whether the information is sufficient.
   - If it is insufficient, use ask_follow_up to request additional details.
   - If it is sufficient, use summarize_memo to organize and summarize it.
2. If a single message contains multiple intentions, you may use multiple tools.
   Example: "Update Xiao Wang’s TOEIC score to 850, and also organize this month’s meeting memo."
   → Use both update_student_info and summarize_memo.
3. After executing the tools, check the results and then report back to the homeroom teacher in a clear and understandable way.
4. Respond in Japanese.

Important: You are the “conductor” of the tools. You do not directly manipulate the database or generate reports yourself. All actions must be executed through the tools.
"""


def get_client() -> OpenAI:
    """
    Set up the OpenAI client.

    :return:
    """

    api_key = os.getenv("DASHSCOPE_API_KEY")

    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY is not set")

    return OpenAI(
        api_key=api_key,
        base_url=os.getenv(
            "DASHSCOPE_BASE_URL",
            "https://dashscope.aliyuncs.com/compatible-mode/v1",
        ),
    )


def run_agent(
        user_message: str,
        db: Session,
        conversation_history: list = None,
) -> dict:
    """
    Run the agent.
    LOOP:

    :param user_message:
    :param db:
    :param conversation_history:
    :return:
    """

    client = get_client()

    if conversation_history:
        messages = conversation_history.copy()
    else:
        messages = [
            {"role": "system", "content": AGENT_SYSTEM_PROMPT},
        ]

    messages.append({"role": "user", "content": user_message})

    tools_used = []
    tools_result = []

    # Set loops
    for iteration in range(MAX_ITERATIONS):
        try:
            response = client.chat.completions.create(
                model="qwen-max",
                messages=messages,
                tools=TOOLS
            )
        except Exception as e:
            return {
                "reply": None,
                "tools_used": tools_used,
                "tools_result": tools_result,
                "error": str(e),
            }

        choice = response.choices[0]
        message = choice.message

        # If tools not necessary: return the message
        if choice.finish_reason == "stop":
            return {
                "reply": message.content,
                "tools_used": tools_used,
                "tools_result": tools_result,
                "error": None,
            }

        # If tools necessary: loop -> finish or stop until max_iters reached
        if choice.finish_reason == "tool_calls":
            tool_calls_list = getattr(choice.message, "tool_calls", None) or []
            messages.append({
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in tool_calls_list
                ]
            })

            for tc in tool_calls_list:
                tool_call_id = tc.id
                tool_name = tc.function.name
                tool_arguments = tc.function.arguments
                tool_input = json.loads(tool_arguments)

                tools_used.append(tool_name)

                result = execute_tool(tool_name, tool_input, db)

                tools_result.append({
                    "tool": tool_name,
                    "input": tool_input,
                    "output": result,
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": result,
                })

            continue

    return {
        "tools_used": tools_used,
        "tools_result": tools_result,
        "error": "Max iterations reached.",
    }