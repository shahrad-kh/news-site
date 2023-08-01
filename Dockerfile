FROM python:3.8

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt --no-cache-dir

COPY . /code/

CMD ["gunicorn", "config.wsgi", ":8000"]