FROM ubuntu:24.04

RUN apt update \
 && apt install -y vim \
    python3-pip pipx \
 && rm -rf /var/lib/apt/lists/*

ENV RUNUSER=myapp
RUN mkdir -p /app
RUN groupadd -g 10001 $RUNUSER && \
   useradd -u 10000 -g $RUNUSER $RUNUSER \
   && chown -R $RUNUSER:$RUNUSER /app

USER $RUNUSER:$RUNUSER

CMD ["bash", "-c", "while true; do sleep 1; done"]
