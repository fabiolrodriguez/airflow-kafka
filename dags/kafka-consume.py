
import airflow
import logging
import sys
import json

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from time import sleep
from json import loads
from kafka import KafkaConsumer

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1),      # this in combination with catchup=False ensures the DAG being triggered from the current date onwards along the set interval
    'provide_context': True,                            # this is set to True as we want to pass variables on from one task to another
}

dag = DAG(
    dag_id='kafka_consume',
    default_args=args,
    schedule_interval= '@once',             # set interval
	catchup=False,                          # indicate whether or not Airflow should do any runs for intervals between the start_date and the current date that haven't been run thus far
)


def consume_message_to_kafka(**context):
    
    consumer = KafkaConsumer(bootstrap_servers='kafka1:9092,kafka2:9092,kafka3:9092',
                                auto_offset_reset='earliest',
                                value_deserializer=lambda x: loads(x.decode('utf-8')),
                                enable_auto_commit=True,
                                group_id=None,
                                consumer_timeout_ms=1000)

    consumer.subscribe(['perform_topic'])


    for message in consumer:
        from kafka import TopicPartition
        from kafka import OffsetAndMetadata
        print(message)
        # logging.info(message)
        # consumer.commit({TopicPartition("example_topic", message.partition): OffsetAndMetadata(message.offset+1, '')})

        # consumer.close(autocommit=True)

    consumer.close()        
        
consume_message_to_kafka = PythonOperator(

    task_id='consume_message_to_kafka',
    python_callable=consume_message_to_kafka,
    dag=dag
)


# def consume_message_to_kafka(**context):

#     consumer = KafkaConsumer(
#     'example_topic',
#      bootstrap_servers='kafka1:9092,kafka2:9092,kafka3:9092',
#      auto_offset_reset='earliest',
#      enable_auto_commit=True,
#     #  group_id='my-group',
#      value_deserializer=lambda x: loads(x.decode('utf-8')))

#     for message in consumer:
#         print (message)


# task1 >> task2                  # set task priority
