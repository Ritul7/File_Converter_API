import logging
import tempfile
import os

import uuid
from app.core.celery_app import celery
from app.models.jobs import Jobs, JobStatus
from app.models.users import Users
from app.database.session import SessionLocal
from app.services.s3_service import get_s3_client
from dotenv import load_dotenv
from app.converters.converter_map import CONVERTER_MAP

load_dotenv()

AWS_BUCKET = os.getenv("AWS_S3_BUCKET_NAME")

# Create logger
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

@celery.task(bind=True)
def process_job(self, job_id: str):

    # logger.info(f"Processing job {job_id}")
    # print("HELLO FROM CELERY")
    # return "done"

    db = SessionLocal()
    job = None

    job_uuid = uuid.UUID(job_id)
    print(f"job_uuid is: {job_uuid}")

    logger.info(f"Started processing job: {job_uuid}")

    try:
        job = db.query(Jobs).filter(Jobs.id == job_uuid).first()

        logger.info(f"AWS_BUCKET = {AWS_BUCKET}")
        logger.info(f"Input file key = {job.input_file_key}")

        if not job:
            logger.warning(f"No job found with id: {job_uuid}")
            return {"message": "No job found"}

        logger.info(f"Job {job_uuid} found. Updating status to PROCESSING")
        job.status = JobStatus.processing
        db.commit()

        # yha tk, job aa chuki hai queue me and ab usko download krna h s3 se, convert krna h and then again upload krna h(converted file)

        s3 = get_s3_client()

        with tempfile.TemporaryDirectory() as temp_dir:         # temp_dir ek temporary folder h bcz libraries like pandas or pdf2image can't directly editt he files in s3, so they are bought here

            input_path = os.path.join(temp_dir, f"input_file.{job.input_format}")               # input_path: It is local destination, telling s3 to take a copy of 'input_file_key' and save it right here
            output_filename = f"{uuid.uuid4()}.{job.output_format}"                             # output_filename: A unique name for the new file
            output_path = os.path.join(temp_dir, output_filename)                               # output_path: A empty spot on hard drive where converter will save the newly converted file

            s3.download_file(AWS_BUCKET, job.input_file_key, input_path)                        # s3.download_file(Bucket, Key, local_path): Takes the file from 'address' i.e. key and put it on 'local_path'

            logger.info(f"Downloaded input file for the job: {job_uuid}")

            converter_class = CONVERTER_MAP.get(                                                # input_format 
                (job.input_format.lower(), job.output_format.lower())
            )

            if not converter_class:
                raise Exception(
                    f"Unsupported Conversion:"
                    f"from {job.input_format} to {job.output_format}"
                )
            
            converter = converter_class()

            converter.convert(input_path, output_path)                      # Taking the file(read) converting it and then storing it on the local_path

            logger.info(f"Conversion completed for job: {job_uuid}")

            # Ab converted file upload hogi on s3
            output_key = f"outputs/{output_filename}"

            print("Output path:", output_path)
            print("Exists:", os.path.exists(output_path))
            print("Size:", os.path.getsize(output_path))

            s3.upload_file(                                     # s3.upload_file(Local_path, Bucket, Key(address)): Takes the converted file and uploads on s3 on address'key'(new)
                output_path,
                AWS_BUCKET,
                output_key,
                ExtraArgs={
                    "ContentType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
            )

            logger.info(f"Uploaded file for job: {job_uuid}")

            job.output_file_key = output_key
            job.status = JobStatus.completed
            db.commit()

            logger.info(f"Job {job_uuid} completed successfully")
            

    except Exception as exc:
        logger.error(f"Error processing job {job_id}: {str(exc)}", exc_info=True)

        if job:
            job.status = JobStatus.failed
            db.commit()
            logger.info(f"Job {job_id} marked as FAILED")

        raise self.retry(exc=exc, countdown=5)

    finally:
        db.close()
        logger.info(f"Database session closed for job {job_id}")

    #     return "10"
    # We imported the Users table here because our SQLAlchemy didn't find the user when storing the metadata