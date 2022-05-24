FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
 && apt -y install \
    vim jq \
    curl wget dnsutils iputils-ping iperf3 iproute2 \
    apt-file pv mlocate tree ffmpeg \
    python3 python3-pip python3-dev python3-wheel python3-cryptography \
    libffi-dev build-essential libssl-dev cargo\
 && apt-file update

RUN pip3 install \
    youtube-dl \
    ansible \
    speedtest-cli

RUN updatedb
