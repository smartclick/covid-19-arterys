FROM ubuntu:16.04

RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y && \
        apt-get update -y  && \
        apt-get install -y python3.7 python3.7-dev python3-pip

RUN apt-get install python3-setuptools

RUN python3.7 -m pip install --upgrade pip
RUN python3.7 -m pip install --upgrade setuptools
# Basic env setup
WORKDIR /opt

# Install requirements and module code
COPY requirements.txt /opt/requirements.txt
RUN python3.7 -m pip install -r /opt/requirements.txt
COPY . /opt/

EXPOSE 8900
ENTRYPOINT [ "python3.7", "mock_server.py" ]
