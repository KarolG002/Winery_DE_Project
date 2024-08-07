import pytest
import pandas as pd
from unittest.mock import patch, MagicMock, mock_open
from src.pipeline.bigquery_load import (
    read_table, merge_tables, upload_to_bigquery
)

@pytest.fixture
def mock_engine():
    """Fixture for creating a mock SQLAlchemy engine."""
    return MagicMock()

@pytest.fixture
def sample_df():
    """Fixture for creating a sample DataFrame."""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'column1': [1, 2, 3],
        'column2': ['a', 'b', 'c']
    })

# Test for the `read_table` function
def test_read_table(mock_engine, sample_df):
    with patch('pandas.read_sql', return_value=sample_df):
        result = read_table('test_table', mock_engine, 0, 10)
    assert result.equals(sample_df)

# Test for the `merge_tables` function
def test_merge_tables(mock_engine, sample_df):
    with patch('src.pipeline.bigquery_load.read_table', return_value=sample_df):
        result = merge_tables(mock_engine, 0, 10)
    # 4 tables are merged, so the length of the result should be 4 times the length of sample_df
    assert len(result) == len(sample_df) * 4  
    # The 'id' column should be dropped
    assert 'id' not in result.columns

# Test for the `upload_to_bigquery` function
@patch('pandas_gbq.to_gbq')
def test_upload_to_bigquery_success(mock_to_gbq, sample_df):
    # Mock credentials
    mock_credentials = MagicMock()
    
    upload_to_bigquery(sample_df, 'test_table', 'test_dataset', 'test_project', mock_credentials)
    
    # Verify the `to_gbq` method was called with the correct parameters
    mock_to_gbq.assert_called_once_with(
        sample_df, 
        'test_dataset.test_table', 
        project_id='test_project', 
        if_exists='append'
    )
