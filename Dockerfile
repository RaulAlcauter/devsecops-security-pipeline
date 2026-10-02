FROM python:3.14-alpine

WORKDIR /app

COPY . /app

RUN adduser -D appuser

USER appuser

RUN pip install -r requirements.txt

CMD ["python3", "app/app.py"]