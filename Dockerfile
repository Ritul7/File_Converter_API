FROM python:3.12-slim               

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .                                                

# Not using CMD here because docker-compose will provide different commands for the FastAPI and the Celery worker.