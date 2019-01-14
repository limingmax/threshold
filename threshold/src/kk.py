
from kafka import KafkaConsumer



consumer = KafkaConsumer('k8s_MonitorData',  bootstrap_servers=['192.168.195.1:32400'])
                         
for message in consumer:
	print message
