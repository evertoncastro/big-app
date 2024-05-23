FROM python:3.12.0-slim as python-base

ENV PYTHONUNBUFFERED 1

ENV POSTGRES_HOST=postgres

WORKDIR /app

COPY requirements.txt /app/
COPY manage.py /app/
COPY application /app/application

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
