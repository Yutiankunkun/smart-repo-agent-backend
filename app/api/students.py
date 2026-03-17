from typing import Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.student import StudentResponse, StudentCreate, StudentUpdate
from app.crud import student as student_crud


router = APIRouter()

@router.post(
    "/",
    response_model=StudentResponse,
    summary="Create a new student",
)
def create_student(
        data: StudentCreate,
        db: Session = Depends(get_db),
):
    """
    Check id existing -> create new student.

    :param data:
    :param db:
    :return:
    """

    student_exist = student_crud.get_student(db, data.id)
    if student_exist:
        raise HTTPException(status_code=400, detail="Student id already exists")

    try:
        student = student_crud.create_student(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return StudentResponse(
        id=student.id,
        name=student.name,
        university=student.university,
        major=student.major,
        toeic=student.toeic,
        jlpt=student.jlpt,
        teacher_id=student.teacher_id,
        teacher_name=student.teacher.name,
    )


@router.get(
    "/",
    response_model=list[StudentResponse],
    summary="Get all students",
)
def get_all_students(
        teacher_id: Optional[str] = None,
        db: Session = Depends(get_db),
):
    """
    Get all students or students of a teacher.

    :param teacher_id:
    :param db:
    :return:
    """

    if teacher_id:
        students = student_crud.get_students_by_teacher(db, teacher_id)
    else:
        students = student_crud.get_all_students(db)

    return [
        StudentResponse(
            id=s.id,
            name=s.name,
            university=s.university,
            major=s.major,
            toeic=s.toeic,
            jlpt=s.jlpt,
            teacher_id=s.teacher_id,
            teacher_name=s.teacher.name,
        )
        for s in students
    ]


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Get a student by id",
)
def get_student(
        student_id: str,
        db: Session = Depends(get_db),
):
    """
    Get a student by id.

    :param student_id:
    :param db:
    :return:
    """

    student = student_crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return StudentResponse(
        id=student.id,
        name=student.name,
        university=student.university,
        major=student.major,
        toeic=student.toeic,
        jlpt=student.jlpt,
        teacher_id=student.teacher_id,
        teacher_name=student.teacher.name,
    )


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update a student's information"
)
def update_student(
        student_id: str,
        data: StudentUpdate,
        db: Session = Depends(get_db),
):
    """
    Update a student's information.

    :param student_id:
    :param data:
    :param db:
    :return:
    """

    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    student = student_crud.update_student(db, student_id, **update_data)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return StudentResponse(
        id=student.id,
        name=student.name,
        university=student.university,
        major=student.major,
        toeic=student.toeic,
        jlpt=student.jlpt,
        teacher_id=student.teacher_id,
        teacher_name=student.teacher.name,
    )


@router.delete(
    "/{student_id}",
    response_model=ApiResponse,
    summary="Delete a student"
)
def delete_student(
        student_id: str,
        db: Session = Depends(get_db),
):
    """
    Delete a student.

    :param student_id:
    :param db:
    :return:
    """

    try:
        student_crud.delete_student(db, student_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return ApiResponse(message="Student deleted successfully.")