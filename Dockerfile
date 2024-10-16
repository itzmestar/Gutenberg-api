# Use the official Python 3.12-slim image as the base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

# Set the working directory
WORKDIR /app

# Install dependencies required to build some Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install "fastapi[all]"

# Copy the rest of the application code
COPY ./gutenberg_app /app/gutenberg_app

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "gutenberg_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
