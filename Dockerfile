FROM python:3.9

RUN pip3.9 install -r ./requirements.txt

EXPOSE 80

COPY ./app /app

CMD ["python3.9", "app/main.py"]
