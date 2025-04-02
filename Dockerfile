# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install system dependencies required for BeatifulSoup4 and other libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Expose the port the app runs on (if applicable)
EXPOSE 8080

# Define healthcheck to ensure the application is running
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=5s \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Define the command to run the application
CMD ["python", "main.py"]