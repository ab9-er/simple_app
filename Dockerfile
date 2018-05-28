FROM nouchka/sqlite3:latest
MAINTAINER 13626352+ab9-er@users.noreply.github.com

ENV APP_DIR /app

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y python3 \
                       python3-pip \
                       build-essential

COPY ./app ${APP_DIR}
COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh && \
    pip3 install -r ${APP_DIR}/requirements.txt

EXPOSE 5000
WORKDIR ${APP_DIR}
ENTRYPOINT ["/entrypoint.sh"]
