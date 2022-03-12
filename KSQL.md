# KSQL

What is KSQL ?
KSQL is the streaming SQL engine that enables real-time data processing against Apache Kafka. It provides an easy-to-use, yet powerful interactive SQL interface for stream processing on Kafka, without the need to write code in a programming language such as Java or Python. KSQL is scalable, elastic, fault-tolerant, and it supports a wide range of streaming operations, including data filtering, transformations, aggregations, joins, windowing, and sessionization.

## CHEATSHEET


````
SHOW TOPICS;
print <topic_name>;
print print_topic from beginning;
SHOW STREAMS;

````


Let’s create new stream :

````
CREATE STREAM STUDENTS_STREAM (id VARCHAR, name VARCHAR, address VARCHAR, city VARCHAR) WITH (kafka_topic='students', value_format='JSON');
````


Let’s create a Table which holds aggregated result of every 30 seconds.

````
CREATE TABLE CITY_AGGREGATE
AS SELECT S.NAME,S.CITY,COUNT(*) AS CITY_COUNT
FROM STUDENTS_STREAM S WINDOW TUMBLING (SIZE 30 SECOND)
GROUP BY S.CITY, S.NAME HAVING COUNT(*) > 1;
SELECT * FROM CITY_AGGREGATE EMIT CHANGES;
````
