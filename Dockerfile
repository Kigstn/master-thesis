FROM python:3.9

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3.9 install -r requirements.txt

COPY ./app /app

EXPOSE 80

CMD ["python3.9", "app/main.py"]
