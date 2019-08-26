FROM python:3

MAINTAINER Gustavo Sampaio

WORKDIR /usr/src/app
RUN mkdir ./log 
RUN mkdir ./certs

COPY requirements_server.txt ./
RUN pip install --no-cache-dir -r requirements_server.txt -t .

COPY . .

CMD [ "python", "./server.py" ]

EXPOSE 80



