FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get upgrade -y

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Specifying command to run when the container starts
CMD ["uvicorn", "run_trained:app", "--host", "0.0.0.0", "--port", "8000"]
