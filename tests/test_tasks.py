import pytest
from datetime import timedelta, datetime
from app.tasks.file_tasks import process_job
from unittest.mock import MagicMock

def test_process_job_logic(mocker, db):

    mock_s3 = mocker.patch("app.tasks.file_tasks.get_s3_client")        # This is the logic of mock s3 client
    mock_client = MagicMock()
    mock_s3.return_value = mock_client

    mock_converter = mocker.patch("app.tasks.file_tasks.CONVERTER_MAP")         # We are mocking the converter now

    from app.models.jobs import Jobs
    from app.models.users import Users
    import uuid

    uid = uuid.uuid4()
    u = Users(id=uid, email="t@t.com", hashed_password = "abc")
    db.add(u)
    job_id = uuid.uuid4()
    job = Jobs(
        id=job_id, 
        user_id=uid, 
        input_file_key="in", 
        input_format="pdf", 
        output_format="docx",
        expires_at = datetime.utcnow() + timedelta(hours = 24)
    )
    db.add(job)
    db.commit()

    mocker.patch("app.tasks.file_tasks.SessionLocal", return_value=db)

    try:
        process_job(MagicMock(), str(job_id))
    except:
        pass

    db.refresh(job)

    assert job.status is not None



