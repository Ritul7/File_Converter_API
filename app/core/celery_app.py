import logging
from celery import Celery
from celery.signals import setup_logging

# ---------------------------------------------------
# Configure Base Logging
# ---------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------
# Create Celery App
# ---------------------------------------------------
logger.info("Initializing Celery application...")

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

logger.info("Celery broker and backend configured with Redis")

celery.autodiscover_tasks(["app.tasks"])

# ---------------------------------------------------
# Configure Task Routes
# ---------------------------------------------------
celery.conf.task_routes = {
    "app.tasks.file_tasks.*": {"queue": "file_queue"}
}

logger.info("Celery task routes configured for file_queue")


# ---------------------------------------------------
# Optional: Control Celery Worker Logging
# ---------------------------------------------------
@setup_logging.connect
def config_loggers(*args, **kwargs):
    logger.info("Celery worker logging configured.")