FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NEXUS_SERVICE_NAME=open-webui-adapter \
    NEXUS_SERVICE_VERSION=v0.5 \
    NEXUS_SERVICE_PORT=8080

WORKDIR /app

COPY integrations/open-webui/adapter.py /app/integrations/open-webui/adapter.py

EXPOSE 8080
CMD ["python", "/app/integrations/open-webui/adapter.py"]
