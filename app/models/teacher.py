from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Teacher(Base):
    """
    Teacher Model, including id, name, specialty.
    """

    __tablename__ = "teachers"

    id = Column(String(20), primary_key=True)

    name = Column(String(50), nullable=False)
    specialty = Column(String(50))

    students = relationship("Student", back_populates="teacher")