FROM python:3.12-slim

WORKDIR /app

# Install deps
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy code
COPY backend /app/backend

EXPOSE 8502

# Run API
CMD ["python", "-m", "uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "8502"]
