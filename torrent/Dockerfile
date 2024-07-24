# syntax = docker/dockerfile:1.3-labs

FROM debian:bullseye
#FROM ubuntu:20.04

RUN apt update \
 && apt -y install openvpn qbittorrent-nox

RUN apt -y install curl vim wget procps less dnsutils iputils-ping


RUN mkdir /config
COPY bootstrap-qb-config.bash /config/

#RUN sed -i 's|^auth-user-pass.*$|auth-user-pass /config/secrets/vpn.creds|g'  /config/openvpn.conf

RUN groupadd -g 8112 torrent \
 && useradd  -m -u 8112 -g 8112 torrent 

WORKDIR /root
CMD ["/config/bootstrap-qb-config.bash"]
 
 
