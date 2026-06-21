FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NEXUS_SERVICE_NAME=crewai \
    NEXUS_SERVICE_VERSION=v0.4 \
    NEXUS_SERVICE_PORT=8080

WORKDIR /app

COPY orchestration/crewai/runtime.py /app/orchestration/crewai/runtime.py

EXPOSE 8080
CMD ["python", "/app/orchestration/crewai/runtime.py"]
