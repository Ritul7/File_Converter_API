from pydantic import BaseModel
from datetime import datetime
import uuid
from app.models.jobs import JobStatus

class JobCreate(BaseModel):             # Jo user send krega wo sab h yha pe
    
    input_file_key: str
    input_format: str
    output_format: str
    # expires_at: datetime              ## expiry should be controlled by the backend not by the user

class JobResponse(BaseModel):

    id: uuid.UUID
    user_id: uuid.UUID
    input_file_key: str
    input_format: str
    output_file_key: str | None
    output_format: str
    status: JobStatus
    created_at: datetime
    expires_at: datetime
    download_url: str | None = None

    class Config:
        from_attributes = True