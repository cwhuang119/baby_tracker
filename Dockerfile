FROM ubuntu:20.04
WORKDIR /workspace
ADD app /workspace
RUN apt update
ENV DEBIAN_FRONTEND noninteractive
RUN apt install python3-pip -y
RUN apt-get install python3-tk -y
#RUN python -m pip install -r requirements.txt
RUN python3 -m pip install line-bot-sdk django
CMD python3 manage.py runserver 0.0.0.0:8000