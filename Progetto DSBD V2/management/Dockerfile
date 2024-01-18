FROM python:3.11-slim

WORKDIR /usr/src/application
COPY application/ ./

RUN pip install grpcio
RUN pip install grpcio-tools
RUN pip install mysql-connector-python
RUN pip install Flask
RUN pip install kafka-python

CMD ["python", "main.py"]