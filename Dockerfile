FROM ubuntu:latest

RUN apt-get update && \
    apt-get dist-upgrade --yes && \
    apt-get install --yes \
	python3-pefile \
	wine \

RUN mkdir /builds && \
    groupadd -g 1000 winston && \
    useradd -u 1000 -g 1000 -d /builds/winston -s /bin/bash -m winston && \
    mkdir -p /builds/winston/workspace && \
    chown -R winston:winston /builds

USER winston

# Declare default working folder
WORKDIR /builds/winston

ENV HOME=/builds/winston \
    SHELL=/bin/bash \
    USER=winston \
    LOGNAME=winston \
    HOSTNAME=blackpod

COPY script.py /builds/winston/script.py

# Set a default command useful for debugging
CMD ["/bin/bash", "--login"]
