# Use an official Python runtime as the base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables (optional, can also be passed via docker-compose)
ENV API_ID=your_api_id
ENV API_HASH=your_api_hash
ENV PHONE_NUMBER=your_phone_number
ENV CHANNEL_USERNAME=your_channel_username
ENV SESSION_NAME=default_session

# Default command (can be overridden in docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3002"]