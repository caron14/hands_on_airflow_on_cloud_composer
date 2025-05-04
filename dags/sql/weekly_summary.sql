-- SQL query to create or replace the weekly summary table.
-- The table name includes the execution date (ds_nodash) for partitioning or identification.
-- The summary_date column stores the logical date (ds) of the DAG run.

CREATE OR REPLACE TABLE `my_dataset.weekly_summary_{{ ds_nodash }}` AS
SELECT
  '{{ ds }}' AS summary_date,
  -- Add other aggregation logic here based on your source tables
  -- Example: COUNT(*) AS total_records
;
