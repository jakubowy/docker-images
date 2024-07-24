FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
 && apt -y install \
    vim jq \
    curl wget dnsutils iputils-ping iperf3 iproute2 net-tools traceroute \
    apt-file \
 && apt install -y python3-pip\
 && apt-file update \
 && pip3 install yt-dlp

#
