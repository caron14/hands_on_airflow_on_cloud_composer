"""
DAG definition for weekly BigQuery and Bash tasks on Cloud Composer.

This DAG demonstrates a typical workflow where a BigQuery job is executed
using a SQL file, followed by a Bash task. The DAG is scheduled to run weekly.

Note:
    - Follows PEP8 and Google style docstrings for maintainability.
    - Tasks are ordered for clarity and future extensibility.
"""
from datetime import datetime
import pendulum
from uuid import uuid4

from airflow.models import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='weekly_bigquery_python_dag',  # Updated DAG ID
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule='@weekly',
    catchup=False,
    tags=['example', 'bigquery'],  # Removed 'dbt' tag
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 0,
        'retry_delay': pendulum.duration(minutes=1),
        'email_on_failure': False,
        'email_on_retry': False,
    },
) as dag:
    # Bash Task - Run a shell command or script
    # Prints the execution date; replace with your actual script as needed.
    echo_exec_dt = BashOperator(
        task_id='run_echo_exec_dt',
        bash_command='echo "Execution date: {{ ds }}"',
    )

    # BigQuery Task - Load SQL from file
    # Executes a BigQuery job using a SQL file for weekly summary aggregation.
    bigquery_task = BigQueryInsertJobOperator(
        task_id='run_bigquery_task',
        configuration={
            "query": {
                # Reference the SQL file with additional Jinja variables
                "query": (
                    "{% include 'sql/weekly_summary.sql' %}"
                ),
                "useLegacySql": False,
                "parameterMode": "NAMED",
                "queryParameters": [
                    {
                        "name": "run_id",
                        "parameterType": {"type": "STRING"},
                        "parameterValue": {"value": uuid4().hex},
                    },
                    {
                        "name": "dag_id",
                        "parameterType": {"type": "STRING"},
                        "parameterValue": {"value": "{{ dag.dag_id }}"},
                    },
                    {
                        "name": "execution_date",
                        "parameterType": {"type": "STRING"},
                        "parameterValue": {"value": "{{ ts }}"},
                    },
                ],
            }
        },
        location='asia-northeast1',  # Specify your BigQuery location (Tokyo)
        gcp_conn_id='google_cloud_default',  # Uses the default Composer connection
    )

    # Bash Task - Run a shell command or script
    # Prints the execution date; replace with your actual script as needed.
    bash_task = BashOperator(
        task_id='run_dummy_func',
        bash_command=(
            'python '
            '{{ dag.folder }}/scripts/dummy_func.py '
            '--execution_date {{ ds }}'
        ),
    )

    # Define Task Dependencies - BigQuery must finish before Bash task runs
    echo_exec_dt >> bigquery_task >> bash_task
