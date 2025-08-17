# syntax=docker/dockerfile:1.4
FROM python:3.12-slim
ENV PYTHONPATH=/app/src

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create virtual environment outside app directory
RUN mkdir /venv && uv venv --seed /venv

# Copy application files
COPY ./src /app/src
WORKDIR /app

# Install dependencies using temporary file
ENV UV_PROGRESS=true
ENV UV_HTTP_TIMEOUT=300
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    mkdir -p /tmp/build && \
    uv pip compile pyproject.toml --output-file=/tmp/build/requirements.txt && \
    uv pip install --python /venv/bin/python -r /tmp/build/requirements.txt && \
    rm -rf /tmp/build

ENV PATH="/venv/bin:$PATH"
EXPOSE 8000 8501
CMD ["sleep", "infinity"]
