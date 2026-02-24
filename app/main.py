from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
from app.models import jobs as jobs_model                 
from app.models import users
from app.routes import jobs, auth, files

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(jobs.router)
app.include_router(auth.router)
app.include_router(files.router)

@app.get('/')
def health_check():
    return {"Message":"Everything is working fine!"}


if __name__ =="__main__":
    import uvicorn
    uvicorn.run("0.0.0.0")