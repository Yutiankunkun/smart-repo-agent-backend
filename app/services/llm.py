import os
import json
from dotenv import load_dotenv
from app.models.student import Student
from app.schemas.meeting import MeetingOutput
from app.core.prompts import build_user_prompt,SYSTEM_PROMPT
from openai import OpenAI


load_dotenv()

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


def call_dashscope(
        student: Student,
        raw_memo: str,
        meeting_date: str,
) -> dict:
    """
    Call the Dashscope API to generate a report.

    :param student:
    :param raw_memo:
    :param meeting_date:
    :return:
    """

    user_message = build_user_prompt(
        student_id=student.id,
        student_name=student.name,
        university=student.university or "",
        major=student.major or "",
        toeic=student.toeic or "",
        jlpt=student.jlpt or "",
        raw_memo=raw_memo,
        meeting_date=meeting_date,
    )

    try:
        client = get_client()
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[  # type: ignore
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        output = completion.choices[0].message.content

    except Exception as e:
        return {
            "report": None,
            "error": str(e),
        }

    cleaned = output.strip()
    parsed = json.loads(cleaned)
    report = MeetingOutput(**parsed)

    return {
        "report": report,
        "error": None,
    }