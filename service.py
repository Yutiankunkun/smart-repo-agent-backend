import os
import json
from dashscope import Generation
from dotenv import load_dotenv
from prompts import build_user_prompt,SYSTEM_PROMPT
from dashscope.api_entities.dashscope_response import Message

from schemas import MeetingOutput

load_dotenv()

def get_apikey() -> str:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY is not set")
    return api_key

def call_dashscope(
        student_id: str,
        student_name: str,
        university: str,
        major: str,
        toeic: str,
        jlpt: str,
        memo: str,
        meeting_date: str,
) -> dict:

    user_message = build_user_prompt(
        student_id=student_id,
        student_name=student_name,
        university=university,
        major=major,
        toeic=toeic,
        jlpt=jlpt,
        memo=memo,
        meeting_date=meeting_date,
    )

    api_key = get_apikey()
    response = Generation.call(
        api_key=api_key,
        model="qwen-max",
        messages=[
            Message(role="system", content=SYSTEM_PROMPT),
            Message(role="user", content=user_message),
        ],
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Dashscope API returned an error: {response.status_code} - {response.text}"
        )

    output = response.output.text
    cleaned = output.strip()
    parsed = json.loads(cleaned)
    report = MeetingOutput(**parsed)

    return {
        "report": report,
        "error": None,
    }