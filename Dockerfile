# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install required dependencies
RUN pip install --no-cache-dir fastapi[all] uvicorn pillow python-multipart

# Expose port 8000 for FastAPI
EXPOSE 8000

# Define environment variable for SECRET_KEY
ENV SECRET_KEY=mysecretkey
ENV ALLOWED_HOSTS=*

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "simple-api:app", "--host", "0.0.0.0", "--port", "8000"]