FROM registry.cn-hangzhou.aliyuncs.com/limingmax-test/ai-base:v2

ENV LANG C.UTF-8

ENV REDIS_IP REDIS_IP
ENV REDIS_PORT REDIS_PORT

ENV KAFKA_IP KAFKA_IP
ENV KAFKA_PORT KAFKA_PORT

ENV CONSUMER_TOPIC CONSUMER_TOPIC
ENV PRODUCER_TOPIC PRODUCER_TOPIC

ENV HBASE_IP HBASE_IP
ENV HBASE_PORT HBASE_PORT

COPY threshold /service/threshold
ADD start.sh /service/threshold/src
RUN chmod -R 777 /service/threshold/src/start.sh

WORKDIR /service/threshold/src

CMD ["/service/threshold/src/start.sh"]
#防docker容器自动退出
ENTRYPOINT tail -f /dev/null
