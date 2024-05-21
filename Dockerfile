FROM python:3.11.9-bullseye

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app
COPY ./best.pt /code/best.pt

RUN apt-get update -y && apt-get install -y libgl1-mesa-glx \
pip install --no-cache-dir --upgrade -r /code/requirements.txt
