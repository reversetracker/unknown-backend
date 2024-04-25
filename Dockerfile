FROM python:3.10.11-slim-buster

ARG GITHUB_TOKEN

RUN echo $GITHUB_TOKEN

RUN apt-get update && apt-get install -y git
RUN git config --global url."https://${GITHUB_TOKEN}:x-oauth-basic@github.com/".insteadOf "https://github.com/"

COPY requirements.txt /opt/unknown-backend/requirements.txt
RUN pip install -r /opt/unknown-backend/requirements.txt

COPY ../.. /opt/unknown-backend
WORKDIR /opt/unknown-backend

CMD ["sh", "-c", "gunicorn unknown_backend.apps.v1:app -c gunicorn.conf.py"]
