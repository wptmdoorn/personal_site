FROM python:3.10

RUN apt-get update

WORKDIR /code
RUN mkdir -p /code/output/

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
COPY ./app /code/app
COPY ./app/static /code/static/

CMD ["python", "app/main.py"]
