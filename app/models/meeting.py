from sqlalchemy import Column, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class Meeting(Base):
    """
    Meeting Model, including id, student_id, student_name, meeting_date.
    """

    __tablename__ = "meetings"

    id = Column(String(20), primary_key=True, default=lambda: str(uuid.uuid4()))

    meeting_date = Column(String(50), nullable=False)
    events = Column(Text)
    process = Column(Text)
    suggestions = Column(Text)
    mental = Column(Text)
    raw_memo = Column(Text)
    pdf_path = Column(String(500))

    student_id = Column(String(20), ForeignKey("students.id"), nullable=False)

    student = relationship("Student", back_populates="meetings")