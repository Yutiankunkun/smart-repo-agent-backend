from sqlalchemy.orm import Session
from typing import Optional
from app.models.meeting import Meeting
from app.schemas.meeting import MeetingInput, MeetingOutput


def create_meeting(
    db: Session,
    input_data: MeetingInput,
    output_data: MeetingOutput,
):
    """
    Create a new meeting in the database.

    :param db:
    :param input_data:
    :param output_data:
    :return:
    """

    meeting = Meeting(
        student_id=input_data.student_id,
        meeting_date=input_data.meeting_date,
        raw_memo=input_data.raw_memo,
        events=output_data.events,
        process=output_data.process,
        suggestions=output_data.suggestions,
        mental=output_data.mental,
    )

    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting


def update_pdf_path(
        db: Session,
        meeting_id: str,
        pdf_path: str,
):
    """
    Generate pdf and update the database.

    :param db:
    :param meeting_id:
    :param pdf_path:
    :return:
    """

    meeting = get_meeting(db, meeting_id)
    if not meeting:
        raise ValueError("Meeting not found")

    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    meeting.pdf_path = pdf_path

    db.commit()
    db.refresh(meeting)
    return meeting


def get_meeting(
        db: Session,
        meeting_id: str,
) -> Optional[Meeting]:
    """
    Get a meeting by id.

    :param db:
    :param meeting_id:
    :return:
    """

    return db.query(Meeting).filter(Meeting.id == meeting_id).first()


def get_meetings_by_student(
        db: Session,
        student_id: str,
) -> list[Meeting]:
    """
    Get a meeting by student.

    :param db:
    :param student_id:
    :return:
    """

    return db.query(Meeting).filter(Meeting.student_id == student_id).all() # type: ignore


def update_meeting(
        db: Session,
        meeting_id: str,
        **kwargs,
) -> Optional[Meeting]:
    """
    Update a meeting's information.

    :param db:
    :param meeting_id:
    :param kwargs:
    :return:
    """

    meeting = get_meeting(db, meeting_id)
    if not meeting:
        raise ValueError("Meeting not found")

    for key, value in kwargs.items():
        if hasattr(meeting, key):
            setattr(meeting, key, value)

    db.commit()
    db.refresh(meeting)
    return meeting


def delete_meeting(
        db: Session,
        meeting_id: str,
) -> bool:
    """
    Delete a meeting from the database.

    :param db:
    :param meeting_id:
    :return:
    """

    meeting = get_meeting(db, meeting_id)
    if not meeting:
        raise ValueError("Meeting not found")

    db.delete(meeting)
    db.commit()
    return True