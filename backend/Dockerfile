FROM python:3.12-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy backend code (including saved_models)
COPY backend /app/backend

# Expose API port
EXPOSE 8502

# Run FastAPI
CMD ["python", "-m", "uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "8502"]
