FROM python:3.11-slim
WORKDIR /app
COPY probe/requirements.txt .
RUN pip install -r requirements.txt
COPY probe/ .
ENTRYPOINT ["python", "main.py"]
