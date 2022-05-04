FROM debian:stable-slim

COPY convert_and_post.py /opt/convert_and_post.py
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
