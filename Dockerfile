FROM python:3.8.3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y postgresql postgresql-contrib

ENV PIPENV_VERSION="2018.10.13"
RUN pip install --no-cache-dir pipenv==$PIPENV_VERSION

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
