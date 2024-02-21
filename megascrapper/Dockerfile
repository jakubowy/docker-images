FROM python:latest

RUN apt update



RUN mkdir -p /opt/app
RUN pip install requests datetime influxdb-client google-cloud-storage google-cloud-secret-manager pyyaml python-dateutil foxesscloud matplotlib
WORKDIR /opt/app
RUN adduser --system --no-create-home nonroot
COPY files/ ./
#RUN pip install -r requirements.txt
USER nonroot

ENTRYPOINT ["python", "/opt/app/app.py"]
CMD ["pse"]
