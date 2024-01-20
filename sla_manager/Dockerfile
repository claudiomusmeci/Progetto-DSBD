FROM python:3.11-slim

WORKDIR /usr/src/application
COPY application/ ./
COPY requirements.txt ../

RUN pip install --no-cache-dir -r ../requirements.txt

CMD ["python", "main.py"]