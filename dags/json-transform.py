
import airflow
import logging
import datetime
import sys
import json

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from time import sleep
from json import loads
from json import dumps
from kafka import KafkaProducer
from kafka import KafkaConsumer




args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1),      # this in combination with catchup=False ensures the DAG being triggered from the current date onwards along the set interval
    'provide_context': True,                            # this is set to True as we want to pass variables on from one task to another
}

dag = DAG(
    dag_id='json_transform',
    default_args=args,
    schedule_interval= '@once',             # set interval
	catchup=False,                          # indicate whether or not Airflow should do any runs for intervals between the start_date and the current date that haven't been run thus far
)


def resend_message_to_kafka(**context):
    
    consumer = KafkaConsumer(bootstrap_servers='kafka1:9092,kafka2:9092,kafka3:9092',
                                auto_offset_reset='earliest',
                                value_deserializer=lambda x: loads(x.decode('utf-8')),
                                enable_auto_commit=True,
                                group_id=None,
                                consumer_timeout_ms=2000)

    consumer.subscribe(['origin_rep_topic'])

    producer = KafkaProducer(bootstrap_servers='kafka1:9092,kafka2:9092,kafka3:9092',
                        value_serializer=lambda x: 
                        dumps(x).encode('utf-8'))

    where_to_send = 'deliver_rep_topic'    

    number=0

    for message in consumer:

        a_datetime = datetime.datetime.now()    # Get actual date
        formatted_datetime = a_datetime.isoformat()
        json_datetime = json.dumps(formatted_datetime)
        message_j = json.dumps(message)
        new_message = json.loads(message_j)
        new_message.append(json_datetime)           # Append date to payload

        producer.send(where_to_send, new_message)   # Send payload to new topic

        number += 1

    print ('transformed messages:')
    print(number)
    
    producer.close()
    consumer.close()

resend_message_to_kafka = PythonOperator(

    task_id='resend_message_to_kafka',
    python_callable=resend_message_to_kafka,
    dag=dag
)

