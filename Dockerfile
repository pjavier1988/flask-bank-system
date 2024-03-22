# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for Python packages if any (e.g., psycopg2)
RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean


RUN pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /app/

COPY prod.env /app/.env

# Configure Poetry: Do not create a virtual environment
ENV POETRY_VIRTUALENVS_CREATE=false

# Install project dependencies, skipping dev dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy your application code to the container
COPY . /app

# Copy your migrations folder (assuming it's at the root of your project)
COPY migrations /app/migrations

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Configure to use Gunicorn, adjust the number of workers as necessary
CMD ["gunicorn", "-w 4", "-b :8000", "app:create_app()"]
