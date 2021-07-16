FROM python:3.9

COPY requirements.txt /app/requirements.txt

RUN pip3.9 install -r /app/requirements.txt

COPY ./app /app/app

EXPOSE 80

WORKDIR /app

CMD ["uvicorn", "app.app.main:app", "--host", "0.0.0.0", "--port", "80"]
