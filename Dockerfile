FROM python:3.8-slim-bullseye

COPY convert_and_post.py /opt/convert_and_post.py
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
