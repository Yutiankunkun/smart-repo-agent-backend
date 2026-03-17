from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.core.database import get_db
from app.models.student import Student
from app.schemas.meeting import RecordResponse
from app.crud import meeting as meeting_crud
from pathlib import Path

router = APIRouter()


@router.get(
    "/students/{student_id}/meetings",
    summary="Get all meetings of a student"
)
def get_meeting_by_student(
        student_id: str,
        db: Session = Depends(get_db),
):
    """
    Get all meetings of a student.

    :param student_id:
    :param db:
    :return:
    """

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    meetings = meeting_crud.get_meetings_by_student(db, student_id)

    return [
        RecordResponse(
            id=m.id,
            student_id=m.student_id,
            student_name=m.student.name,
            meeting_date=m.meeting_date,
            events=m.events,
            process=m.process,
            suggestions=m.suggestions,
            mental=m.mental,
            teacher_id=m.student.teacher_id,
            teacher_name=m.student.teacher.name,
            raw_memo=m.raw_memo,
            pdf_path=m.pdf_path,
        )
        for m in meetings
    ]


@router.get(
    "/{meeting_id}",
    summary="Get a meeting by id"
)
def get_meeting(
        meeting_id: str,
        db: Session = Depends(get_db),
):
    """
    Get a meeting by id.

    :param meeting_id:
    :param db:
    :return:
    """

    meeting = meeting_crud.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    return RecordResponse(
        id=meeting.id,
        student_id=meeting.student_id,
        student_name=meeting.student.name,
        meeting_date=meeting.meeting_date,
        events=meeting.events,
        process=meeting.process,
        suggestions=meeting.suggestions,
        mental=meeting.mental,
        teacher_id=meeting.student.teacher_id,
        raw_memo=meeting.raw_memo,
        teacher_name=meeting.student.teacher.name,
        pdf_path=meeting.pdf_path,
    )


@router.delete(
    "/{meeting_id}",
    summary="Delete a meeting"
)
def delete_meeting(
        meeting_id: str,
        db: Session = Depends(get_db),
):
    """
    Delete a meeting.

    :param meeting_id:
    :param db:
    :return:
    """

    meeting = meeting_crud.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    meeting_crud.delete_meeting(db, meeting_id)
    return {"message": "Meeting deleted successfully."}


@router.get(
    "/pdf/{meeting_id}",
    summary="Download a pdf of a meeting"
)
def download_pdf(
        meeting_id: str,
        db: Session = Depends(get_db),
):
    """
    You can download a pdf of a meeting.

    :param meeting_id:
    :param db:
    :return:
    """

    meeting = meeting_crud.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    if not meeting.pdf_path:
        raise HTTPException(status_code=404, detail="PDF not generated yet")

    pdf_file = Path(meeting.pdf_path)
    if not pdf_file.exists():
        raise HTTPException(status_code=404, detail="PDF not found")

    return FileResponse(
        path=str(pdf_file),
        filename=pdf_file.name,
        media_type="application/pdf",
    )