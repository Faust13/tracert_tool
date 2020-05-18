FROM python:3.6-alpine3.10

RUN mkdir /app
WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD [ "python3", "run.py" ]