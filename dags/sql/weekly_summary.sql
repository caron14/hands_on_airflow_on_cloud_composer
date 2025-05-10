-- SQL query to create or replace the weekly summary table.
-- The table name includes the execution date (ds_nodash) for partitioning or identification.
-- The summary_date column stores the logical date (ds) of the DAG run.

CREATE OR REPLACE TABLE `composer-practice-458112.hands_on_airflow_on_cloud_composer.baseball_schedules_{{ ds_nodash }}` AS

  SELECT
    `{{ ds }}` AS csdate,
    *,
  FROM
    `composer-practice-458112.baseball.schedules`
  LIMIT 10
;
