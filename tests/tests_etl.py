import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import os

# Import the functions from the refactored script
from src.pipeline.etl import read_data, insert_to_db, main

# Helper function to create a dummy DataFrame
def create_dummy_df():
    return pd.DataFrame({
        'col1': [1, 2],
        'col2': ['a', 'b']
    })

# Test read_data function
@patch('os.listdir', return_value=['red.csv', 'rose.csv', 'sparkling.csv', 'white.csv'])
@patch('pandas.read_csv')
def test_read_data(mock_read_csv, mock_listdir):
    mock_read_csv.return_value = create_dummy_df()

    red, rose, sparkling, white = read_data('dummy_filepath/')

    assert not red.empty
    assert not rose.empty
    assert not sparkling.empty
    assert not white.empty
    assert list(red.columns) == ['col1', 'col2']
    assert list(rose.columns) == ['col1', 'col2']
    assert list(sparkling.columns) == ['col1', 'col2']
    assert list(white.columns) == ['col1', 'col2']

@patch('pandas.read_csv', side_effect=FileNotFoundError)
def test_read_data_file_not_found(mock_read_csv):
    result = read_data('dummy_filepath/')
    assert result is None
# Test insert_to_db function
@patch('src.pipeline.etl.create_engine')
def test_insert_to_db_success(mock_create_engine):
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    df = create_dummy_df()
    with patch.object(df, 'to_sql') as mock_to_sql:
        insert_to_db(df, 'dummy_table')
        mock_to_sql.assert_called_once_with(name='dummy_table', con=mock_engine, if_exists='append', index=False)
    
    # Assert that create_engine was called with the expected connection string
    mock_create_engine.assert_called_once_with('postgresql://root:root@localhost:5432/winedb')

@patch('src.pipeline.etl.create_engine')
def test_insert_to_db_failure(mock_create_engine):
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine
    df = create_dummy_df()
    
    # Patch DataFrame.to_sql to raise an exception
    with patch.object(pd.DataFrame, 'to_sql', side_effect=Exception('Insertion Error')):
        with patch('builtins.print') as mock_print:
            insert_to_db(df, 'dummy_table')
            mock_print.assert_called_with('Error inserting DataFrame into dummy_table table: Insertion Error')

    # Assert that create_engine was called with the expected connection string
    mock_create_engine.assert_called_once_with('postgresql://root:root@localhost:5432/winedb')
if __name__ == "__main__":
    pytest.main()