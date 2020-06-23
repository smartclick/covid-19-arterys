FROM python:3.7-slim

WORKDIR /opt

# Install requirements and module code
COPY requirements.txt /opt/requirements.txt
RUN python3.7 -m pip install -r /opt/requirements.txt
COPY . /opt/

RUN apt-get update && apt-get install -y python3-gdcm

RUN cp /usr/lib/python3/dist-packages/gdcm.py /usr/local/lib/python3.7/site-packages/
RUN cp /usr/lib/python3/dist-packages/gdcmswig.py /usr/local/lib/python3.7/site-packages/
RUN cp /usr/lib/python3/dist-packages/_gdcmswig*.so /usr/local/lib/python3.7/site-packages/
RUN cp /usr/lib/x86_64-linux-gnu/libgdcm* /usr/local/lib/python3.7/site-packages/

EXPOSE 8900
ENTRYPOINT [ "python3.7", "mock_server.py" ]
