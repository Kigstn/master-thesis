FROM python:3.9

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3.9 install -r /app/requirements.txt

COPY . .

EXPOSE 80

CMD ["python3.9", "app/main.py"]
