from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from app.database.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Users(Base):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)