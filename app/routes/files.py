from fastapi import APIRouter, File, UploadFile, Depends
from app.services.s3_service import generate_upload_url
from app.models.users import Users
from app.auth.jwt_auth import get_curr_user

router = APIRouter(prefix="/file")

# "/upload_url" pr jayega user to ek url milegi jispe jaake file upload kr payega

@router.post("/get_upload_url")
async def create_upload_url(
    my_file: UploadFile = File(...),
    curr_user: Users = Depends(get_curr_user)):
    
    print(f"The {curr_user.email} is requesting a url")
    result = await generate_upload_url(my_file)

    return result["upload_url"]


