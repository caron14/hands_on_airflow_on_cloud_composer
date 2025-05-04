# Instructions for Deploying and Running the DAG in Google Cloud Composer

This document provides step-by-step instructions on how to deploy and run the `weekly_bigquery_python_dag` in your Google Cloud Composer environment.

## Prerequisites

1.  **Google Cloud Platform (GCP) Account:** You need an active GCP account with billing enabled.
2.  **Cloud Composer Environment:** A running Cloud Composer environment (v1 or v2). Make note of your environment's name and region.
3.  **Google Cloud SDK (gcloud):** The `gcloud` command-line tool installed and configured to interact with your GCP project.
4.  **BigQuery Dataset:** Ensure the BigQuery dataset `my_dataset` exists in your GCP project and the Composer service account has permissions to create tables in it. If it doesn't exist, create it using the Google Cloud Console or `bq` command-line tool:
    ```bash
    bq mk my_dataset
    ```
5.  **Permissions:** The service account used by your Cloud Composer environment needs appropriate permissions, primarily:
    *   `roles/bigquery.dataEditor` (or more specific permissions to read/write to `my_dataset`)
    *   `roles/composer.worker` (usually granted by default)
    *   `roles/storage.objectAdmin` (for accessing the DAGs bucket)

## Deployment Steps

1.  **Identify your Composer GCS Bucket:** Every Composer environment has an associated Google Cloud Storage (GCS) bucket where DAGs and plugins are stored. Find your bucket name using the `gcloud` tool (replace `YOUR_COMPOSER_ENV_NAME` and `YOUR_REGION`):
    ```bash
    gcloud composer environments describe YOUR_COMPOSER_ENV_NAME \
      --location YOUR_REGION \
      --format="value(config.dagGcsPrefix)"
    ```
    This command will output the path to the `dags` folder within your environment's bucket (e.g., `gs://asia-northeast1-your-env-xxxxxx-bucket/dags`).

    *Example*
    ```bash
    gcloud composer environments describe hands-on-airflow-on-cloud-composer --location asia-northeast1 --format="value(config.dagGcsPrefix)"
    ```

2.  **Upload DAG Files:** Copy the entire `dags` directory from this project into your Composer environment's GCS bucket `dags` folder. You can use the `gsutil` command:
    ```bash
    # Navigate to the root of this project directory first
    cd /path/to/hands_on_airflow_on_cloud_composer

    # Replace YOUR_COMPOSER_GCS_DAGS_FOLDER with the path from step 1
    gsutil -m cp -r dags/* YOUR_COMPOSER_GCS_DAGS_FOLDER/
    ```
    *Example:*
    ```bash
    gsutil -m cp -r dags/* gs://us-central1-your-env-xxxxxx-bucket/dags/
    ```
    Airflow automatically detects and loads new DAGs from this bucket, which might take a few minutes.

## Running the DAG

1.  **Access the Airflow UI:**
    *   Navigate to the Cloud Composer section in the Google Cloud Console.
    *   Select your environment.
    *   Click on the "Airflow UI" link.

2.  **Locate and Trigger the DAG:**
    *   In the Airflow UI, find the DAG named `weekly_bigquery_python_dag`.
    *   Ensure the DAG is unpaused (toggle the switch on the left to "On").
    *   To run the DAG manually, click the "Play" button (Trigger DAG) on the right side of the DAG listing. You can optionally provide a specific configuration if needed, but for a standard run, just click "Trigger".

3.  **Monitor the DAG Run:**
    *   Click on the DAG name (`weekly_bigquery_python_dag`) to view its details and recent runs.
    *   Click on the latest run in the "Runs" tab to see the Graph View or Grid View.
    *   Monitor the status of the tasks (`execute_bigquery_task`, `run_python_task`). They should turn green upon successful completion.

## Verification

1.  **Check BigQuery:**
    *   Navigate to the BigQuery section in the Google Cloud Console.
    *   Select your project and the `my_dataset` dataset.
    *   Look for a table named `weekly_summary_YYYYMMDD` (where `YYYYMMDD` corresponds to the logical date of the DAG run).
    *   Query the table to verify its contents (it will contain the `summary_date` column).
    ```sql
    SELECT * FROM `my_dataset.weekly_summary_YYYYMMDD` LIMIT 10;
    ```

2.  **Check Python Task Logs:**
    *   In the Airflow UI, go to the details of the specific DAG run.
    *   Click on the `run_python_task` instance in the Grid View or Graph View.
    *   Click "Logs".
    *   You should see the log message: `INFO - Executing custom Python script for execution date: YYYY-MM-DD` and the printed output `Python task executed for date: YYYY-MM-DD`.

You have now successfully deployed and run the Airflow DAG in your Cloud Composer environment.
