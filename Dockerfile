FROM python:3.10.6-buster

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY interface interface
COPY setup.py setup.py
RUN pip install .

CMD uvicorn interface.api.fast:app --host 0.0.0.0 --port $PORT
