FROM python:3.8.3-alpine3.11

RUN mkdir /app
WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD [ "python3", "run.py" ]