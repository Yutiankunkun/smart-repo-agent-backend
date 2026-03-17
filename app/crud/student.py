from sqlalchemy.orm import Session
from typing import Optional
from app.models.student import Student
from app.models.teacher import Teacher
from app.schemas.student import StudentCreate


def create_student(
        db: Session,
        data: StudentCreate,
) -> Student:
    """
    Create a new student in the database.
    Example: student_A = create_student(db, "sid0001", "藍天", "東京科学大学", "情報", "845", "N1")

    :param db:
    :param data:
    :return:
    """

    teacher = db.query(Teacher).filter(Teacher.id == data.teacher_id).first()
    if not teacher:
        raise ValueError("Invalid teacher id")

    student = Student(
        id=data.id,
        name=data.name,
        university=data.university,
        major=data.major,
        toeic=data.toeic,
        jlpt=data.jlpt,
        teacher_id=data.teacher_id,
    )

    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_all_students(db: Session) -> list[Student]:
    """
    Get all students from the database.

    :param db:
    :return:
    """
    return db.query(Student).all()  # type: ignore


def get_student(
        db: Session,
        student_id: str,
) -> Optional[Student]:
    """
    Get a student's information by id.

    :param db:
    :param student_id:
    :return:
    """

    return db.query(Student).filter(Student.id == student_id).first()


def get_students_by_teacher(
        db: Session,
        teacher_id: str,
) -> list[Student]:
    """
    Get all students of a teacher.

    :param db:
    :param teacher_id:
    :return:
    """

    return db.query(Student).filter(Student.teacher_id == teacher_id).all()


def update_student(
        db: Session,
        student_id: str,
        **kwargs,
) -> Optional[Student]:
    """
    Update a student's information.

    :param db:
    :param student_id:
    :param kwargs:
    :return:
    """

    student = get_student(db, student_id)
    if not student:
        raise ValueError("Student not found")

    for key, value in kwargs.items():
        if hasattr(student, key):
            setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


def delete_student(
        db: Session,
        student_id: str,
) -> bool:
    """
    Delete a student from the database.

    :param db:
    :param student_id:
    :return:
    """

    student = get_student(db, student_id)
    if not student:
        raise ValueError("Student not found")

    db.delete(student)
    db.commit()
    return True