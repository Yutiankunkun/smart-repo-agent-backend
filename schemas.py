from typing import Optional
from pydantic import BaseModel, Field
from datetime import date


class MeetingInput(BaseModel):
    """
    You put the raw memo here.
    """

    student_id: str = Field(
        description="student id",
        examples=["id0001"]
    )

    student_name: str = Field(
        description="student name",
        examples=["藍天"]
    )

    university: str = Field(
        description="university graduated",
        examples=["東京科学大学"]
    )

    major: str = Field(
        description="field of study",
        examples=["情報通信系"]
    )

    toeic: str = Field(
        description="TOEIC --> English",
        examples=["845"]
    )

    jlpt: str = Field(
        description="JlPT --> Japanese",
        examples=["N1"]
    )

    memo: str = Field(
        description="raw --> memo; processed --> note",
        examples=["This is a memo, which you could completely write everything."
                  "You don't have to worry about whether the memo is structured."
                  "Because this system will help you !! :) "]
    )

    meeting_date: str = Field(
        default_factory=lambda: date.today().strftime("%Y年%m月%d日"),
        description="The date you have a meeting with the student",
        examples=["2026年3月29日"],
    )


class MeetingOutput(BaseModel):
    """
    The LLM model output the structured report here.
    """

    student_id: str = Field(
        description="student id"
    )

    student_name: str = Field(
        description="student name"
    )

    meeting_date: str = Field(
        description="The date you have a meeting with the student"
    )

    events: str = Field(
        description="The things that student was engaging in"
    )

    process: str = Field(
        description="To tell the things goes well or not"
    )

    suggestions: str = Field(
        description="Advice and infos you offer to the student"
    )

    mental: str = Field(
        description="Check the student to make sure the mental health"
    )


class Response(BaseModel):
    """
    To check if the response works.
    """

    report: Optional[MeetingOutput] = Field(
        default=None,
        description="output to report",
    )

    error: Optional[str] = Field(
        default=None,
        description="error infos, output null if success",
    )