# Use an official Python image as the base
FROM python:3.9-slim

# ✅ Add these lines to update system packages and patch vulnerabilities
RUN apt-get update && apt-get upgrade -y

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file from the root directory and install dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend source code into the container
COPY . .

# Specify the command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]