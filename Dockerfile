FROM python:3.9

COPY requirements.txt /app/requirements.txt

RUN pip3.9 install -r /app/requirements.txt

COPY ./app /app

EXPOSE 80

CMD ["python3.9", "main.py"]
