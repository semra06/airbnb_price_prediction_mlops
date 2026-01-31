FROM python:3.10-slim

WORKDIR /app

# Better runtime behavior
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Backend source code
COPY backend /app/backend

# Expose FastAPI port
EXPOSE 8502

# Healthcheck (optional ama önerilir)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8502/docs || exit 1

# Run FastAPI
CMD ["uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "8502"]
