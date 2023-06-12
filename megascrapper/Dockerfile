ROM python:latest

RUN apt update
RUN pip install PyYAML requests

RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY app.py ./
RUN adduser --system --no-create-home nonroot
USER nonroot

CMD ["python", "/opt/app/app.py"]
