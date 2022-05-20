FROM debian:latest
#FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
RUN apt update \
 && apt-get install -y git build-essential cmake automake libtool autoconf wget ca-certificates

WORKDIR /
RUN git clone https://github.com/MoneroOcean/xmrig.git
RUN mkdir -p /xmrig/build

RUN sed -i 's/kDefaultDonateLevel = 1/kDefaultDonateLevel = 0/g' /xmrig/src/donate.h
RUN sed -i 's/kMinimumDonateLevel = 1/kMinimumDonateLevel = 0/g' /xmrig/src/donate.h
WORKDIR /xmrig/scripts

RUN ./build_deps.sh

WORKDIR /xmrig/build

RUN cmake .. -DXMRIG_DEPS=scripts/deps \
 && make -j$(nproc)

