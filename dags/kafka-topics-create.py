import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from time import sleep
from json import dumps
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1),      # this in combination with catchup=False ensures the DAG being triggered from the current date onwards along the set interval
    'provide_context': True,                            # this is set to True as we want to pass variables on from one task to another
}

dag = DAG(
    dag_id='kafka_topics_create',
    default_args=args,
    schedule_interval= '@once',             # set interval
	catchup=False,                          # indicate whether or not Airflow should do any runs for intervals between the start_date and the current date that haven't been run thus far
)


def create_topic_kafka(**context):

    admin_client = KafkaAdminClient(
        bootstrap_servers="kafka1:9092,kafka2:9092,kafka3:9092", 
        client_id='test'
    )

    topic_list = []
    topic_list.append(NewTopic(name="origin_rep_topic", num_partitions=24, replication_factor=1))
    topic_list.append(NewTopic(name="deliver_rep_topic", num_partitions=24, replication_factor=1))
    admin_client.create_topics(new_topics=topic_list, validate_only=False)

create_topic_kafka = PythonOperator(

    task_id='create_topic_kafka',
    python_callable=create_topic_kafka,
    dag=dag
)











