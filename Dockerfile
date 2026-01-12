# QWEN API Docker Image with llama-cpp-python CUDA support
FROM nvidia/cuda:12.6.1-devel-ubuntu24.04 AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install numpy first (required by llama-cpp-python)
RUN pip install --no-cache-dir "numpy<2"

# Build and install llama-cpp-python with CUDA support
# CMAKE_ARGS enables CUDA backend
ENV CMAKE_ARGS="-DGGML_CUDA=on"
ENV FORCE_CMAKE=1
RUN pip install --no-cache-dir llama-cpp-python>=0.3.0 --verbose

# Install remaining dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Runtime stage ----
FROM nvidia/cuda:12.6.1-runtime-ubuntu24.04

WORKDIR /app

# Install Python runtime only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

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
