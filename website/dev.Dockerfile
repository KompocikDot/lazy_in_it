FROM python:3.12-alpine3.19

WORKDIR /lazy_in_it/website

RUN adduser -D lazyinuit && chown -R lazyinuit /lazy_in_it/website

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header", "--reload"]