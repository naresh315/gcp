"""A liveness prober dag for monitoring composer.googleapis.com/environment/healthy."""
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.sftp.hooks.sftp import SFTPHook
from airflow.providers.google.cloud.transfers.sftp_to_gcs  import SFTPToGCSOperator

from datetime import timedelta

default_args = {
    'start_date': airflow.utils.dates.days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'naresh_dag',
    default_args=default_args,
    description='liveness monitoring dag',
    schedule_interval='*/10 * * * *',
    max_active_runs=2,
    catchup=False,
    dagrun_timeout=timedelta(minutes=10),
)

# priority_weight has type int in Airflow DB, uses the maximum.
t1 = BashOperator(
    task_id='echo',
    bash_command='echo test',
    dag=dag,
    depends_on_past=False,
    priority_weight=2**31 - 1,
    do_xcom_push=False)

    
sftp_to_gcs_task = SFTPToGCSOperator(
    task_id='sftp_to_gcs_task',
    sftp_conn_id='naresh-sftp-1',
    source_path='/home/yt4naresh/bhabat/*',
    destination_bucket='us-central1-naresh-composer-9a46c0e4-bucket',
    destination_path='/logs',
    dag=dag
)
