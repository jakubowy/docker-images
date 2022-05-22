FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
 && apt -y install vim curl wget dnsutils iputils-ping apt-file jq pv python3 python3-pip python3-dev python3-wheel \
 && apt-file update

RUN pip3 install \
    youtube-dl
