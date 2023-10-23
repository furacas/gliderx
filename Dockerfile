FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y wget && \
    wget https://github.com/nadoo/glider/releases/download/v0.16.3/glider_0.16.3_linux_amd64.tar.gz && \
    tar zxvf glider_*_linux_amd64.tar.gz && \
    mv glider_*_linux_amd64/glider /usr/local/bin/ && \
    rm glider_*_linux_amd64.tar.gz

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY convert.py convert.py
COPY glider.conf.template glider.conf.template
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh


CMD ["./entrypoint.sh"]
