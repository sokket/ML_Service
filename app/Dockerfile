FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

EXPOSE 8080

CMD [ "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080" ]