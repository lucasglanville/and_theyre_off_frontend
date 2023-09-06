FROM python:3.10.6-buster

COPY requirements.txt requirements.txt
COPY interface interface
COPY setup.py setup.py

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD uvicorn interface.app.fast:app --host 0.0.0.0 --port $PORT
