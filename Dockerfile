FROM python:3.11

WORKDIR /main
COPY . ./

RUN apt-get update
RUN apt-get install -y --no-install-recommends default-jre default-jdk
RUN pip install -r requirements.txt

EXPOSE 1412

#docker build -t tomatoserver:latest .