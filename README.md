# Airflow, BigQuery, and Python Workflow

## Overview
This document provides instructions for the design and implementation of an Apache Airflow workflow integrated with BigQuery and custom Python scripts on Google Cloud Composer 2.x. The workflow automates the execution of a scheduled BigQuery SQL query and a Python-based task weekly.

## System Components
- **Apache Airflow (Google Cloud Composer):** Manages workflow scheduling and task orchestration.
- **BigQuery:** Data warehouse used for running SQL queries and storing results.
- **Python Scripts:** For custom processing and utility operations within workflows.

## Workflow Steps
1.  **Bash Task:**
    - Prints the execution date for logging or debugging purposes.
2.  **BigQuery Task:**
    - Executes a scheduled SQL query using a parameterized SQL file.
    - Generates or updates summary tables in BigQuery.
3.  **Python Task:**
    - Executes a Python script to perform additional custom logic (e.g., logging or data validation).

## Setup and Requirements

### Cloud Composer Environment:
- **Composer version:** 2.x
- **APIs:** Cloud Composer, BigQuery
- **IAM Roles:**
    - Composer Service Account: BigQuery Job User, BigQuery Data Editor

### Connections:
- **Airflow Connections:**
    - `google_cloud_default`: Default connection provided by Composer.

## Folder Structure
```
dags/
├── dag_definition.py
├── sql/
│   └── weekly_summary.sql
└── scripts/
    └── dummy_func.py
```

## Airflow DAG Deployment
Deploy the DAG Python file to the Cloud Composer environment’s associated Cloud Storage bucket.
```bash
gsutil cp dag_definition.py gs://your-composer-bucket/dags/
```
Ensure all related `.sql` and `.py` files are also uploaded appropriately to maintain modularity.

## Flow Diagram
```mermaid
graph LR;
    Bash[Echo Task: Print Execution Date] --> BigQuery[BigQuery Task: Execute SQL Query];
    BigQuery --> Python[Python Task: Run Custom Script];
```

## Best Practices
- **Idempotency:** Ensure all tasks can safely rerun without adverse effects.
- **Parameterization:** Utilize Jinja templates for dynamic execution contexts (e.g., dates).
- **Modularity:** Keep logic in separate SQL and Python script files.
- **Error Handling:** Implement retries and clear logging strategies.

## Contact
For assistance or questions regarding this workflow, contact the data engineering team.


---

# Comprehensive Guide: Creating an Apache Airflow DAG on Google Cloud Composer 2.x

## Introduction
Google Cloud Composer is a managed version of Apache Airflow provided by Google Cloud Platform (GCP). It allows users to orchestrate, schedule, and manage workflows without worrying about infrastructure.

## Core Components
- **DAG:** Defines the workflow's structure, tasks, and schedule.
- **BigQueryInsertJobOperator:** Executes BigQuery SQL jobs.
- **PythonOperator:** Executes custom Python functions within Airflow.

## Prerequisites
- A GCP Project with Cloud Composer and BigQuery APIs enabled.
- Composer environment set up with Airflow 2.x.
- IAM permissions for Composer's service account:
    - BigQuery Job User
    - BigQuery Data Editor (for writing results).

## DAG File Structure
Your DAG file (`.py`) should contain:
- Imports: Airflow and operator modules.
- Default arguments: Common settings for tasks.
- DAG definition: Includes `dag_id`, schedule interval, and task details.

## Step-by-Step Guide

### 1. Imports
```python
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
```

### 2. Default Arguments
```python
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
}
```

### 3. DAG Definition
```python
with DAG(
    dag_id='weekly_dag_bigquery_and_python_execution',
    default_args=default_args,
    schedule_interval='@weekly',
    catchup=False,
    tags=['example'],
) as dag:

    # Bash Task
    bash_task = BashOperator(
        task_id='print_execution_date',
        bash_command='echo "Execution date is {{ ds }}"',
    )

    # BigQuery Task
    bigquery_task = BigQueryInsertJobOperator(
        task_id='execute_bigquery_task',
        configuration={
            "query": {
                "query": """
                    CREATE OR REPLACE TABLE `my_dataset.weekly_summary_{{ ds_nodash }}` AS
                    SELECT '{{ ds }}' AS summary_date
                """,
                "useLegacySql": False,
            }
        },
        location='US',
        gcp_conn_id='google_cloud_default',
    )

    # Python Task
    def python_task_callable(execution_date, **kwargs):
        print(f'Execution date: {execution_date}')

    python_task = PythonOperator(
        task_id='run_python_task',
        python_callable=python_task_callable,
        op_kwargs={'execution_date': '{{ ds }}'},
    )

    # Task Dependencies
    bash_task >> bigquery_task >> python_task
```

## Deployment
Upload the DAG file (`dag_definition.py`) to the Cloud Composer environment's DAGs folder in its associated GCS bucket:
```bash
gsutil cp dag_definition.py gs://your-composer-bucket-name/dags/
```
Composer detects new DAGs automatically within a few minutes.

## Best Practices
- **Idempotency:** Tasks should be safe to rerun.
- **Parameterization:** Use Jinja templating (e.g., `{{ ds }}`) for dynamic operations.
- **Connections:** Use Airflow's `google_cloud_default` connection.
- **Modularity:** Move complex logic to separate Python scripts/modules.
- **Clear Naming:** Descriptive and concise task IDs.
- **Error Handling:** Utilize retries and proper logging.
- **SQL Queries:** For complex SQL, store queries in `.sql` files referenced from operators.

## Conclusion
You've successfully created and deployed an Airflow DAG orchestrating BigQuery and Python tasks, scheduled to run weekly. This integration enhances your data workflows with the power and organization of Airflow and BigQuery.

