FROM golang:1.19.1-bullseye

RUN mkdir -p /opt/myapp

COPY gasmeter.gtpl go.mod /opt/myapp/

WORKDIR /opt/myapp

RUN go get github.com/eclipse/paho.mqtt.golang

COPY myapp.go gasmeter.gtpl go.mod /opt/myapp/

RUN go mod tidy
RUN go build myapp.go 

RUN ls -la && whoami && echo "========================"

CMD ["./myapp"]
