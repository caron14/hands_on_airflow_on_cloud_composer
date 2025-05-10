\
import pytest
from airflow.models.dagbag import DagBag

@pytest.fixture(scope="session")
def dagbag():
    """Fixture to load the DAG bag."""
    # Point DagBag to the dags directory relative to the project root
    # Assuming tests are run from the project root
    return DagBag(dag_folder='dags', include_examples=False)

def test_dag_loaded(dagbag):
    """Test if the DAG is loaded correctly by DagBag."""
    dag_id = 'weekly_bigquery_python_dag'
    dag = dagbag.get_dag(dag_id)
    assert dag is not None, f"DAG '{dag_id}' not found in DagBag."
    assert len(dagbag.import_errors) == 0, f"DAG Import Errors: {dagbag.import_errors}"

def test_dag_tasks(dagbag):
    """Test if the DAG has the expected tasks."""
    dag_id = 'weekly_bigquery_python_dag'
    dag = dagbag.get_dag(dag_id)
    assert dag is not None
    expected_tasks = {'execute_bigquery_task', 'run_python_task'}
    actual_tasks = {task.task_id for task in dag.tasks}
    assert actual_tasks == expected_tasks, f"Expected tasks {expected_tasks}, but got {actual_tasks}"

def test_task_dependencies(dagbag):
    """Test the dependencies between tasks in the DAG."""
    dag_id = 'weekly_bigquery_python_dag'
    dag = dagbag.get_dag(dag_id)
    assert dag is not None

    bigquery_task = dag.get_task('execute_bigquery_task')
    python_task = dag.get_task('run_python_task')

    # Check downstream dependencies for bigquery_task
    assert python_task.task_id in bigquery_task.downstream_task_ids
    # Check upstream dependencies for python_task
    assert bigquery_task.task_id in python_task.upstream_task_ids
