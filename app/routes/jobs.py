from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.jobs import Jobs
from app.schemas.job import JobCreate, JobResponse
from app.auth.jwt_auth import get_curr_user
from app.models.users import Users
from datetime import datetime, timedelta
from app.tasks.file_tasks import process_job


router = APIRouter()  

# Only authenticated user are now able to create the jobs <<<<Protected Route bolte h>>>>

@router.post("/auth/jobs", response_model=JobResponse)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    curr_user: Users = Depends(get_curr_user)):

    new_job = Jobs(
        **job.model_dump(),
        user_id = curr_user.id,
        expires_at = datetime.utcnow() + timedelta(hours = 24)
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    print("handling task")
    
    try:
        process_job.delay(str(new_job.id))          # Ye background me task ko trigger krega, uuid ek object hota h
    except Exception as e:
        print("error ------------:",e)  
    else:
        print("Task completed")                                          # str(new_job.id) isliye bcz celery uuid(object) ko serialize nhi krega, so we convert it into JSON serializable data

    return new_job


























# ..............Ye tab likhna tha, when everyone was allowed to create the job, no authentication was involved in game.

# @router.post("/", response_model=JobResponse)                   # It is telling FastAPI ki is endpoint ka jo response h wo JobResponse ke schema se match hona chahiye
# def create_job(job: JobCreate, db: Session = Depends(get_db)):
    
#     db_job = Jobs(**job.model_dump())       # model_dump() is a pydantic method which converts pydantic model object into python dictionary
#     db.add(db_job)
#     db.commit()
#     db.refresh(db_job)

#     return db_job                       # Directly object return kr rhe h, but bcz apn ne argument me "response_model=JobResponse" pass kiya h, it will take that object, convert it into JobResponse and applieas all the validation and finally converts it into json and sends the response

# .........AUTHENTICATED USERS ka job create krne ka logic routes/auth ke andr likha h bcz, prefix lag rha h na wha "/auth", yha bh explicitly kr skte h.






