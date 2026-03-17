from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Student(Base):
    """
    Student Model, including id, name, university, major, toeic, jlpt, teacher_id.
    """

    __tablename__ = "students"

    id = Column(String(20), primary_key=True)

    name = Column(String(50), nullable=False)
    university = Column(String(50))
    major = Column(String(50))
    toeic = Column(String(50))
    jlpt = Column(String(50))

    teacher_id = Column(String(20), ForeignKey("teachers.id"), nullable=False)

    teacher = relationship("Teacher", back_populates="students")
    meetings = relationship("Meeting", back_populates="student")