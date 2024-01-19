FROM python:3.11.1-slim-bullseye

WORKDIR /usr/src/application
COPY application/ ./
COPY requirements.txt ../

RUN pip install --no-cache-dir -r ../requirements.txt

CMD ["python", "main.py"]