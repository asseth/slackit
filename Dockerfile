FROM frolvlad/alpine-python3

ENV SLACK_TOKEN YOUR_SLACK_TOKEN
ENV GITTER_TOKEN YOUR_GITTER_TOKEN

COPY slackit.py /root/
COPY requirements.txt /root/

RUN pip install -r /root/requirements.txt
CMD ["/usr/bin/python3", "/root/slackit.py"]
