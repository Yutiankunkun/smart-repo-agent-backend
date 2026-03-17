from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.teacher import TeacherResponse, TeacherCreate, TeacherUpdate
from app.crud import teacher as teacher_crud


router = APIRouter()

@router.post(
    "/",
    response_model=TeacherResponse,
    summary="Create a new teacher",
)
def create_teacher(
        data: TeacherCreate,
        db: Session = Depends(get_db),
):
    """
    Check id existing -> create new teacher.

    :param data:
    :param db:
    :return:
    """

    teacher_exist = teacher_crud.get_teacher(db, data.id)
    if teacher_exist:
        raise HTTPException(status_code=400, detail="Teacher id already exists")

    teacher = teacher_crud.create_teacher(db, data)

    return teacher


@router.get(
    "/",
    response_model=list[TeacherResponse],
    summary="Get all teachers",
)
def get_all_teachers(db:Session = Depends(get_db)):
    """
    Get all teachers.
    :param db:
    :return:
    """

    return teacher_crud.get_all_teachers(db)


@router.get(
    "/{teacher_id}",
    response_model=TeacherResponse,
    summary="Get a teacher by id",
)
def get_teacher(
        teacher_id: str,
        db: Session = Depends(get_db),
):
    """
    Get a teacher by id.

    :param teacher_id:
    :param db:
    :return:
    """

    teacher = teacher_crud.get_teacher(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return teacher


@router.put(
    "/{teacher_id}",
    response_model=TeacherResponse,
    summary="Update a teacher's information"
)
def update_teacher(
        teacher_id: str,
        data: TeacherUpdate,
        db: Session = Depends(get_db),
):
    """
    Update a teacher's information.

    :param teacher_id:
    :param data:
    :param db:
    :return:
    """

    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    teacher = teacher_crud.update_teacher(db, teacher_id, **update_data)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return teacher


@router.delete(
    "/{teacher_id}",
    response_model=ApiResponse,
    summary="Delete a teacher",
)
def delete_teacher(
        teacher_id: str,
        db: Session = Depends(get_db),
):
    """
    Delete a teacher.

    :param teacher_id:
    :param db:
    :return:
    """

    try:
        teacher_crud.delete_teacher(db, teacher_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"message": "Teacher deleted successfully."}
