FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NEXUS_SERVICE_NAME=openhands \
    NEXUS_SERVICE_VERSION=v0.7 \
    NEXUS_SERVICE_PORT=8080

WORKDIR /app

COPY integrations/openhands/adapter.py /app/integrations/openhands/adapter.py

EXPOSE 8080
CMD ["python", "/app/integrations/openhands/adapter.py"]
