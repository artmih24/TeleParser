FROM python:3.12.0-alpine3.18

RUN apk update
RUN apk upgrade
RUN apk add cmd:pip3
RUN apk add sed

COPY . ./TeleParser

RUN python3 -m venv .
RUN source ./bin/activate
RUN sed -i.bak 's/\r$//g' ./TeleParser/requirements.txt
RUN sed -i.bak 's/\r$//g' ./TeleParser/TeleParser.py
RUN python3 -m pip install -r ./TeleParser/requirements.txt

CMD ["python3", "./TeleParser/TeleParser.py"]
