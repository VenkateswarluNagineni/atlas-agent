# Agent API image. Retrieval + agent extras are layered in later phases.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir -e ".[serve]"

# Placeholder until the streaming FastAPI agent service lands (roadmap phase 11).
CMD ["python", "-c", "import atlas; print('atlas', atlas.__version__)"]
