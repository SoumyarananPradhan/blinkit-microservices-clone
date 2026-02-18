FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The command to run the app. Host 0.0.0.0 is crucial for Docker.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]