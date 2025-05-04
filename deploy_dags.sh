#!/bin/bash

# Get the GCS bucket path for the Composer environment
gcs_dag_path=$(gcloud composer environments describe hands-on-airflow-on-cloud-composer \
  --location asia-northeast1 \
  --format="value(config.dagGcsPrefix)")

# Check if the gcs_dag_path is not empty
if [ -z "$gcs_dag_path" ]; then
  echo "Error: Failed to retrieve the GCS DAG path."
  exit 1
fi

# Copy the DAG files to the Composer GCS bucket
echo "Copying DAG files to GCS bucket: gsutil -m cp -r dags/* $gcs_dag_path"
gsutil -m cp -r dags/* "$gcs_dag_path"