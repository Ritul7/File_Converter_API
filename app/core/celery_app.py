import logging
from celery import Celery
from celery.signals import setup_logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

logger.info("Initializing Celery application...")

# celery = Celery(
#     "worker",
#     broker="redis://redis:6379",
#     backend="redis://redis:6379",
# )
celery = Celery(
    "worker",
    broker="redis://localhost:6379",
    backend="redis://localhost:6379",
)

logger.info("Celery broker and backend configured with Redis")

celery.autodiscover_tasks(["app.tasks"])

celery.conf.task_routes = {
    "app.tasks.file_tasks.*": {"queue": "file_queue"}
}

logger.info("Celery task routes configured for file_queue")

celery.conf.imports = ["app.tasks.file_tasks"]