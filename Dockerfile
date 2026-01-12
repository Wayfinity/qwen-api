# QWEN API Docker Image
FROM nvidia/cuda:12.6.1-runtime-ubuntu24.04

WORKDIR /app

# Install Python and pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create and use virtual environment to avoid system package conflicts
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY models/ ./models/
COPY utils/ ./utils/
COPY run.py .

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app /opt/venv
USER appuser

# Expose API port
EXPOSE 8000

# Run the application
CMD ["python", "run.py"]
