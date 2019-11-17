from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="kafka-junction-mymail-0739.aivencloud.com:11182",
    security_protocol="SSL",
    ssl_cafile="../../kafka_cred/ca.pem",
    ssl_certfile="../../kafka_cred/service.cert",
    ssl_keyfile="../../kafka_cred/service.key",
)

for i in range(1, 4):
    message = "message number {}".format(i)
    print("Sending: {}".format(message))
    producer.send("demo-topic", message.encode("utf-8"))

# Force sending of all messages

producer.flush()