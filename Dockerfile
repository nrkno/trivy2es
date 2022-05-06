FROM python:3.8-slim-bullseye

RUN apt-get update && apt-get -y upgrade && apt-get install -y python3-requests
COPY convert_and_post.py /opt/convert_and_post.py
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
