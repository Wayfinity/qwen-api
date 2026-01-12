# Multi-stage build for QWEN API

# Stage 1: Builder stage with CUDA dev tools
FROM nvidia/cuda:12.6.1-devel-ubuntu24.04 AS builder

WORKDIR /app

# Install Python, build tools, and dev libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.10 \
    python3-dev \
    python3-pip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /tmp/* /root/.cache/pip

# Stage 2: Runtime stage - minimal Python image
FROM python:3.10-slim

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY app/ ./app/
COPY models/ ./models/
COPY utils/ ./utils/
COPY run.py .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["python", "run.py"]
