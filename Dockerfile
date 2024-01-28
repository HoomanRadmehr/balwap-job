FROM python:3.8
USER root
COPY . ./app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m pip install -U pip
RUN apt update
