from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperatorair

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 6, 12),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'great_expectations_validation',
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
)

def run_expectations():
    exec(open("great_Expectations.py").read())

run_expectations_task = PythonOperator(
    task_id='run_expectations',
    python_callable=run_expectations,
    dag=dag,
)

run_expectations_task