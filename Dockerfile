# Stage 1: Builder
FROM python:3.12.3-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up UV environment
ENV PATH="/root/.local/bin:${PATH}"

# Create virtual environment
RUN python -m uv venv /app/venv

# Activate virtual environment
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .

# Install dependencies into virtual environment
RUN uv pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12.3-slim

WORKDIR /docuChat

# Create and switch to non-root user
RUN useradd -m -u 1000 user && \
    mkdir -p /docuChat/venv && \
    chown -R user:user /docuChat
USER user

# Copy virtual environment from builder
COPY --from=builder --chown=user:user /app/venv /docuChat/venv

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/docuChat/venv/bin:${PATH}"

# Copy application files
COPY --chown=user:user . .

EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "App.py", "--server.port=8501", "--server.address=0.0.0.0"]