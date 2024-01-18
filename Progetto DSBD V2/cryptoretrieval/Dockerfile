FROM python:3.11-slim

WORKDIR /usr/src/application
COPY application/ ./

RUN pip install requests
RUN pip install kafka-python

CMD ["python", "main.py"]