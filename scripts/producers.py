from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="kafka-junction-mymail-0739.aivencloud.com:11182",
    security_protocol="SSL",
    ssl_cafile="../../kafka_cred/ca.pem",
    ssl_certfile="../../kafka_cred/service.cert",
    ssl_keyfile="../../kafka_cred/service.key",
)
import requests

from kafka import KafkaProducer
from kq import Queue

# Set up a Kafka producer.
# producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')

# Set up a queue.
queue = Queue(topic='demo-topic', producer=producer)

# Enqueue a function call.
# job = queue.enqueue(requests.get, 'https://www.google.com')
job = queue.using(timeout=10, key=b'foo', partition=0).enqueue(requests.get, 'https://www.google.com')