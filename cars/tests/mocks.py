from unittest.mock import Mock, patch


def mock_model_exists(mock, model_name):
    mock.return_value = Mock(ok=True)
    mock.return_value.json.return_value = {
        'Results': [
            {
                'Model_Name': model_name
            }
        ]
    }


def mock_model_doesnt_exist(mock):
    mock.return_value = Mock(ok=True)
    mock.return_value.json.return_value = {
        'Results': [
            {
                'Model_Name': 'NonExistantModel'
            }
        ]
    }
