FROM python:3.11.9-bullseye

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt-get update -y && apt-get install -y libgl1-mesa-glx

COPY ./app /code/app

COPY ./best.pt /code/best.pt