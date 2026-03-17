from typing import Optional
from sqlalchemy.orm import Session
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate


def create_teacher(
        db: Session,
        data: TeacherCreate,
):
    """
    Create a new teacher in the database.
    Example: teacher_A = create_teacher(db, "tid0001", "天天", "情報")

    :param db:
    :param data:
    :return:
    """

    teacher = Teacher(
        id=data.id,
        name=data.name,
        specialty=data.specialty,
    )

    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher


def get_all_teachers(db:Session) -> list[Teacher]:
    """
    Get all teachers from the database.

    :param db:
    :return:
    """

    return db.query(Teacher).all()  # type: ignore


def get_teacher(
        db: Session,
        teacher_id: str,
) -> Optional[Teacher]:
    """
    Get a teacher's information by id.

    :param db:
    :param teacher_id:
    :return:
    """

    return db.query(Teacher).filter(Teacher.id == teacher_id).first()


def update_teacher(
        db: Session,
        teacher_id: str,
        **kwargs,
) -> Optional[Teacher]:
    """
    Update a teacher's information.

    :param db:
    :param teacher_id:
    :param kwargs:
    :return:
    """

    teacher = get_teacher(db, teacher_id)
    if not teacher:
        raise ValueError("Teacher not found")

    for key, value in kwargs.items():
        if hasattr(teacher, key):
            setattr(teacher, key, value)

    db.commit()
    db.refresh(teacher)
    return teacher


def delete_teacher(
        db: Session,
        teacher_id: str,
) -> bool:
    """
    Delete a teacher from the database.

    :param db:
    :param teacher_id:
    :return:
    """

    teacher = get_teacher(db, teacher_id)
    if not teacher:
        raise ValueError("Teacher not found")

    db.delete(teacher)
    db.commit()
    return True