# This script receives messages from a Kafka topic

from kafka import KafkaConsumer
import logging
from kq import Worker

formatter = logging.Formatter('[%(levelname)s] %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger = logging.getLogger('kq.worker')
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

consumer = KafkaConsumer(
    "demo-topic",
    auto_offset_reset="earliest",
    bootstrap_servers="kafka-junction-mymail-0739.aivencloud.com:11182",
    client_id="demo-client-1",
    group_id="demo-group",
    security_protocol="SSL",
    ssl_cafile="../../kafka_cred/ca.pem",
    ssl_certfile="../../kafka_cred/service.cert",
    ssl_keyfile="../../kafka_cred/service.key",
)

# Call poll twice. First call will just assign partitions for our
# consumer without actually returning anything


# worker = Worker(topic='demo-topic', consumer=consumer)
# worker.start()


for _ in range(2):
    raw_msgs = consumer.poll(timeout_ms=1000)
    print(raw_msgs)
    for tp, msgs in raw_msgs.items():
        for msg in msgs:
            print("Received: {}".format(msg.value))

# Commit offsets so we won't get the same messages again

consumer.commit()