import boto3
import uuid
import os
from fastapi import File, UploadFile
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET = os.getenv("AWS_S3_BUCKET_NAME")

def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )

async def generate_upload_url(file: UploadFile):
    s3 = get_s3_client()

    print("Client created")
    file_key = f"uploads/{uuid.uuid4()}_{file.filename}"

    try:
        print("Inside try block")
        upload_url = s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": AWS_BUCKET,
                "Key": file_key
            },
            ExpiresIn=300
        )
        print("try fininshed")
        return {
            "upload_url": upload_url,
            "file_key": file_key
        }

    except Exception as e:
        print(f"DEBUG ERROR: {type(e).__name__} - {str(e)}") # This will show the real error
        return {"error": str(e)}
    
def generate_download_url(file_key: str):           # File ko download krne ke liye jo URL generate kr rhe h, usme sirf file ka name jaruri hai... not the whole file  
    s3 = get_s3_client()

    print("s3 client created")
    
    return s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": AWS_BUCKET,
            "Key": file_key,
            "ResponseContentDisposition": "attachment; filename=converted.docx",
            "ResponseContentType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        },
        ExpiresIn=300
    )
