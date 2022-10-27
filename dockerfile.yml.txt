FROM python:3.8

RUN apt-get update
RUN apt-get -y install cron
RUN apt-get -y install nano

RUN mkdir -p /home/shushan
COPY . /home/shushan
WORKDIR /home/shushan

#RUN wget https://dl.minio.io/client/mc/release/linux-amd64/mc -P /usr/bin/
#RUN chmod +x /usr/bin/mc

RUN pip freeze > requirements.txt
RUN pip install -r requirements.txt

# CMD ["sh", "setup.sh"]