FROM python:3.6

MAINTAINER kamal.nandan@alumni.ie.edu

RUN apt-get update
RUN pip install requests requests_oauthlib kafka

ADD twitter_app.py /
CMD python3 twitter_app.py
