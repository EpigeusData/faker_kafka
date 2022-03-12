# faker_kafka

based on:
* https://towardsdatascience.com/assessing-the-quality-of-data-in-streams-2c6352bcbb5b

# Kafka

## Start docker-compose

````
docker-compose up
````

### test connections

Zookeeper

````
nc -zv localhost 22181
````

Kafka

````
nc -zv localhost 9092
````

test kafka logs if started

````
docker-compose logs kafka | grep -i started
````

## Create a topic custchannel.

````
docker exec faker_kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --topic custchannel \
  --create
````

## list topics

````
docker exec faker_kafka kafka-topics \
  --bootstrap-server=localhost:9092 \
  --list
````

## describe the custchannel topic

````
docker exec faker_kafka kafka-topics \
  --bootstrap-server=localhost:9092 \
  --describe \
  --topic custchannel
````

# Python part / The producer


## Create a producer using Python, that sends data continuously

* Create a new Python script named **producer_cust_ch.py**

### Then initialize a Kafka producer

* `bootstrap_servers=[‘localhost:9092’]:`` sets the host and port the producer should contact to bootstrap initial cluster metadata.
* `value_serializer=lambda x: dumps(x).encode(‘utf-8’):`` a function that states the way data is to be serialized before sending to the broker. Here, we convert the data to a JSON file and encode it to utf-8.



## Start the producer

````
./producer_cust_ch.py
````

This will generate fake data and send it to kafka.


## test what has been written to kafka topic with kafkacat

first install kafkacat

````
kafkacat -b localhost:9092 -t custchannel
````

# MongoDB part (TODO)

## 4. Having a namespace including database and collection to store incoming customer records on MongoDB
