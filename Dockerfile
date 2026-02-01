# syntax=docker/dockerfile:1.6
# QWEN API Docker Image with llama-cpp-python CUDA support
FROM nvidia/cuda:12.4.1-devel-ubuntu22.04 AS builder

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
    ninja-build \
    ccache \
    git \
    curl \
    libcublas-12-4 \
    libcublas-dev-12-4 \
    libcublaslt-12-4 \
    libcublaslt-dev-12-4 \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install build tools
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip setuptools wheel

# Install numpy first (required by llama-cpp-python)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install "numpy<2"

# Build and install llama-cpp-python with CUDA support
ARG CUDA_ARCHS="70;75;80;86;89;90"
ENV CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=${CUDA_ARCHS}"
ENV GGML_CCACHE=ON
ENV CCACHE_DIR=/root/.cache/ccache
ENV FORCE_CMAKE=1
ENV CUDACXX=/usr/local/cuda/bin/nvcc
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/ccache \
    pip install "llama-cpp-python>=0.3.0"

# Install remaining dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# ---- Runtime stage ----
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

WORKDIR /app

# Install Python runtime only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-venv \
    libcublas-12-4 \
    libcublaslt-12-4 \
    libgomp1 \
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
