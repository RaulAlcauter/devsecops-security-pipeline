FROM python:3.14-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /usr/local/lib/python3.14/site-packages/pip \
              /usr/local/lib/python3.14/site-packages/pip-*.dist-info

COPY app ./app

RUN adduser -D appuser

USER appuser

CMD ["python3", "app/app.py"]