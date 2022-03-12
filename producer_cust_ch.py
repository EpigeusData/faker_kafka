#!/usr/bin/env python3

from kafka import KafkaProducer
import json
import time
from data import get_registered_user

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=json_serializer)

if __name__ == "__main__":
    while 1 == 1:
        registered_user = get_registered_user()
        print(registered_user)
        producer.send("custchannel", registered_user)
        time.sleep(10)
