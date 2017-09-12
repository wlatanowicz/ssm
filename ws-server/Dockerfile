FROM python:3.6-alpine3.6

RUN apk update \
  && apk add git

WORKDIR /server

COPY . .

RUN pip install -r requirements.txt

CMD python server.py
