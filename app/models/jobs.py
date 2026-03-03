import uuid
from datetime import datetime 
from sqlalchemy import Column, Integer, Text, DateTime, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base
from sqlalchemy.orm import relationship
import enum

class JobStatus(str, enum.Enum):                # enum means enumeration i.e. a fixed set of some values
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Jobs(Base):

    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    input_file_key = Column(String, nullable=False)
    input_format = Column(String, nullable=False)
    output_file_key = Column(String, nullable=True)
    output_format = Column(String, nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.pending, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    expires_at = Column(DateTime, nullable=False)

