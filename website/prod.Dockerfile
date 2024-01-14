FROM python:3.11-alpine3.19

RUN adduser -D lazyinuit && chown -R lazyinuit /lazy_in_it/website

WORKDIR /lazy_in_it/website

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--no-server-header"]
