# syntax=docker/dockerfile:1
FROM debian:bookworm
WORKDIR /workspace
RUN apt-get update && apt-get -y install python3-dev python3-pip chafa imagemagick ffmpeg libsm6 libxext6 
RUN mkdir /opt/imgrot 
COPY . /opt/imgrot
RUN pip3 install -r /opt/imgrot/requirements.txt --break-system-packages
ENTRYPOINT [ "python3", "/opt/imgrot/imgrot.py" ]
