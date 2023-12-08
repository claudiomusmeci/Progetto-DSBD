FROM python:3.11.1-slim-bullseye

WORKDIR /usr/src/application
COPY application/ ./

RUN pip install kafka-python
RUN pip install mysql-connector-python

CMD ["python", "main.py"]