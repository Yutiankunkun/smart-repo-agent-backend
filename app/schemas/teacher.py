from typing import Optional
from pydantic import BaseModel, Field


class TeacherCreate(BaseModel):
    """
    You put the teacher info here, for the first time.
    """

    id: str = Field(
        description="teacher who is responsible for the student",
        examples=["tid0001"]
    )

    name: str = Field(
        description="teacher who is responsible for the student",
        examples=["先生A"]
    )

    specialty: str = Field(
        description="Specialty of the teacher",
        examples=["情報"]
    )


class TeacherUpdate(BaseModel):
    """
    You can update the teacher info here.
    """

    name: Optional[str] = None
    specialty: Optional[str] = None


class TeacherResponse(BaseModel):
    """
    Return the teacher info to the frontend.
    """

    id: str
    name: str
    specialty: str

    model_config = {"from_attributes": True}