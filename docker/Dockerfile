FROM python:3.11.6

RUN pip install pandas

WORKDIR /app

COPY pipeline.py pipeline.py

ENTRYPOINT [ "python", "pipeline.py"]
