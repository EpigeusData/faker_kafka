#!/usr/bin/env python3

from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads

consumer = KafkaConsumer(
    'custchannel',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='custdq',
    value_deserializer=lambda x: loads(x.decode('utf-8')))


client = MongoClient('localhost:27017')
collection = client.custchannel.custchannel

for message in consumer:
    message = message.value
    collection.insert_one(message)
    print('{} added to {}'.format(message, collection))
