FROM registry.cn-hangzhou.aliyuncs.com/limingmax-test/ai-base:v3

ENV LANG C.UTF-8

ADD hbase.keytab /etc
ADD krb5.conf /etc

COPY threshold /service/threshold
ADD start.sh /service/threshold/src
RUN chmod -R 777 /service/threshold/src/start.sh

WORKDIR /service/threshold/src

CMD ["/service/threshold/src/start.sh"]
#防docker容器自动退出
ENTRYPOINT tail -f /dev/null
