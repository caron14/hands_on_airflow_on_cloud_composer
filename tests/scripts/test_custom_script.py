\
import logging
from unittest.mock import patch

import pytest

# Adjust the import path based on the project structure
# Assuming tests are run from the root directory
from dags.scripts.custom_script import run_custom_logic

def test_run_custom_logic_logs_and_prints(caplog):
    """
    Test if run_custom_logic logs the correct info message and prints the expected output.

    Args:
        caplog: Pytest fixture to capture log output.
    """
    test_date = "2024-01-15"
    expected_log_message = f"Executing custom Python script for execution date: {test_date}"
    expected_print_message = f"Python task executed for date: {test_date}\\n" # Add newline for print

    caplog.set_level(logging.INFO)

    # Use patch to capture print output
    with patch('builtins.print') as mock_print:
        run_custom_logic(execution_date=test_date)

        # Check log messages
        assert expected_log_message in caplog.text

        # Check print output
        mock_print.assert_called_once_with(f"Python task executed for date: {test_date}")

# Example of another test if the function had more logic
# def test_run_custom_logic_handles_specific_case():
#     # Add test logic for other scenarios if needed
#     pass
