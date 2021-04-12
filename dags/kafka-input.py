
import airflow
import json
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from time import sleep
from kafka import KafkaProducer
from json import dumps


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1),      # this in combination with catchup=False ensures the DAG being triggered from the current date onwards along the set interval
    'provide_context': True,                            # this is set to True as we want to pass variables on from one task to another
}

dag = DAG(
    dag_id='kafka_input',
    default_args=args,
    schedule_interval= '@once',             # set interval
	catchup=False,                          # indicate whether or not Airflow should do any runs for intervals between the start_date and the current date that haven't been run thus far
)


def send_message_to_kafka(**context):
    # line below was the solution for me
    producer = KafkaProducer(bootstrap_servers='kafka1:9092,kafka2:9092,kafka3:9092',
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

    payload = {
        'topic': 'origin_rep_topic',        "msg": 'load_webtraffic',        "domainName": 'cleaf.it'
        }
        
    where_to_send = payload['topic']
    
    number=0

    for n in range(1000000):
        payload = {
            'topic': 'origin_rep_topic',        "msg": 'load_webtraffic',        "domainName": 'cleaf.it'
            }
        producer.send('origin_rep_topic', value=payload)  
        # print('message sent')         


    # for e in range(1000):
    #     data = {'number' : e}
    #     producer.send('example_topic', value=data)
    #     sleep(5)

        number += 1

    print ('sent messages:')
    print(number)
        

    producer.flush()
    producer.close()


send_message_to_kafka = PythonOperator(

    task_id='send_message_to_kafka',
    python_callable=send_message_to_kafka,
    dag=dag
)
