from typing import Optional
from pydantic import BaseModel, Field
from datetime import date


class MeetingInput(BaseModel):
    """
    You put the raw memo here.
    """

    student_id: str = Field(
        description="student id",
        examples=["sid0001"]
    )

    raw_memo: str = Field(
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

    teacher_id: Optional[str] = Field(
        default="",
        description="teacher who is responsible for the student -> id"
    )

    teacher_name: Optional[str] = Field(
        default="",
        description="teacher who is responsible for the student -> name"
    )


class RecordResponse(BaseModel):
    """
    Return the output to the frontend.
    """

    student_id: str
    student_name: str
    meeting_date: str
    events: str
    process: str
    suggestions: str
    mental: str
    raw_memo: str
    teacher_id: str
    teacher_name: str

    id: str = Field(
        description="The id of the report",
        examples=["repo0001"]
    )

    pdf_path: Optional[str] = Field(
        default=None,
        description="The path of the pdf file",
    )

    model_config = {"from_attributes": True}