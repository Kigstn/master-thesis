FROM python:3.9

COPY requirements.txt /app

RUN pip3.9 install -r /app/requirements.txt

COPY ./app /app/app
COPY dist /app
COPY static /app
COPY templates /app

WORKDIR /app

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
