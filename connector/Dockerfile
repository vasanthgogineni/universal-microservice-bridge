# universal_connector/connector/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY connector/requirements.txt .
RUN pip install -r requirements.txt
COPY connector/ .
ENTRYPOINT ["python", "main.py"]
