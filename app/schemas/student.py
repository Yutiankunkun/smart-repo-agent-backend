from typing import Optional
from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    """
    You put the student info here, for the first time.
    """

    id: str = Field(
        description="student id",
        examples=["sid0001"]
    )

    name: str = Field(
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

    teacher_id : str = Field(
        description="teacher who is responsible for the student",
        examples=["tid0001"]
    )


class StudentUpdate(BaseModel):
    """
    You can update the student info here.
    """

    name: Optional[str] = None
    university: Optional[str] = None
    major: Optional[str] = None
    toeic: Optional[str] = None
    jlpt: Optional[str] = None
    teacher_id: Optional[str] = None


class StudentResponse(BaseModel):
    """
    Return the student info to the frontend.
    """

    id: str
    name: str
    university: str
    major: str
    toeic: str
    jlpt: str
    teacher_id: str
    teacher_name: str

    model_config = {"from_attributes": True}