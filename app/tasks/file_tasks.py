import logging

from app.core.celery_app import celery
from app.models.jobs import Jobs, JobStatus
from app.database.session import SessionLocal

# Create logger
logger = logging.getLogger(__name__)

@celery.task(bind=True, max_retries=3)
def process_job(self, job_id: str):
    db = SessionLocal()
    job = None

    logger.info(f"Started processing job: {job_id}")

    try:
        job = db.query(Jobs).filter(Jobs.id == job_id).first()

        if not job:
            logger.warning(f"No job found with id: {job_id}")
            return {"message": "No job found"}

        logger.info(f"Job {job_id} found. Updating status to PROCESSING")
        job.status = JobStatus.processing
        db.commit()

        # Simulating processing
        job.output_file_key = f"outputs/{job.id}.{job.output_format}"
        job.status = JobStatus.completed
        db.commit()

        logger.info(f"Job {job_id} completed successfully")

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

        return "10"