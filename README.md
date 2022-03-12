# faker_kafka

based on:
* https://towardsdatascience.com/assessing-the-quality-of-data-in-streams-2c6352bcbb5b

# The architecture

How does a streaming data quality architecture look like?

* Create a customer application that captures customer demography details
* Declare 2 consuming applications — one for MDM and the other for the analytical sandbox.
* Run an incremental quality analysis on arriving data from the online portal where customers are registering themselves for a product
* Run a data quality test on arriving data using ksql using consistency and validity data quality rules
* Send notifications back to customers, based on validation results
* Capture the metrics in the dashboard for visualization

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


````
docker exec -it mongodb mongo
````

create the DB

````
use custchannel
````



# 5. Creating 2 consumer groups (applications) to consumer data


Now, let's create a new file consumer_cust_ch.py and import JSON.loads, the KafkaConsumer class, and MongoClient from pymongo.




6. Creating another consumer group to read the same messages - multiple consumers

 group mdm is subscribed to the same topic custchannel.

````
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --topic custchannel --group mdm
````

# KSQL Part

connect to KSQL

````
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
````

````
ksql> CREATE STREAM custdqdemo (name VARCHAR, address VARCHAR, phone VARCHAR, job VARCHAR, email VARCHAR, dob VARCHAR, created_at VARCHAR) \
WITH (VALUE_FORMAT = 'JSON', KAFKA_TOPIC = 'custchannel');
````

We can look at the messages from the topic custchannel, being displayed as we query the stream.

````
ksql> select * from custdqdemo EMIT CHANGES;
````

8. Assessing a stream and creating an exception stream with data quality validations

In the ksql script, I am using a simple case statement to check for
a. policy exception if the customer’s date of birth is behind 1980.
b. valid profession/job names.


````
CREATE STREAM custexcep AS
SELECT name,
       CASE
         WHEN dob < '1980-01-01'      THEN 'Policyexception'
         WHEN job = 'Arboriculturist' THEN 'Not standard profession'
         ELSE                                      'Correct'
       END AS Quality
  FROM CUSTDQDEMO;
````

````
ksql> select * from custexcep EMIT CHANGES;
````
