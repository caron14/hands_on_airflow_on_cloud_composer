from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.python import PythonOperator

# Import the custom Python function
from scripts.custom_script import run_custom_logic


with DAG(
    dag_id='weekly_bigquery_python_dag',  # Updated DAG ID
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule='@weekly',
    catchup=False,
    tags=['example', 'bigquery'],  # Removed 'dbt' tag
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 1,
        'retry_delay': pendulum.duration(minutes=5),
        'email_on_failure': False,
        'email_on_retry': False,
    },
) as dag:
    # BigQuery Task - Load SQL from file
    bigquery_task = BigQueryInsertJobOperator(
        task_id='execute_bigquery_task',
        configuration={
            "query": {
                # Reference the SQL file
                "query": "{% include 'sql/weekly_summary.sql' %}",
                "useLegacySql": False,
            }
        },
        location='US',  # Specify your BigQuery location
        gcp_conn_id='google_cloud_default',  # Uses the default Composer connection
    )

    # Python Task - Call the imported function
    python_task = PythonOperator(
        task_id='run_python_task',
        python_callable=run_custom_logic,
        # Pass execution_date using Jinja templating
        op_kwargs={'execution_date': '{{ ds }}'},
    )

    # Define Task Dependencies - Updated to remove dbt_task
    bigquery_task >> python_task
