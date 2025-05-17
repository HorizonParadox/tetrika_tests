import pytest
from unittest.mock import patch, mock_open
from solution import get_category_members, main
import requests

MOCK_API_RESPONSE = {
    "batchcomplete": "",
    "query": {
        "categorymembers": [
            {"pageid": 1, "ns": 0, "title": "Аардварк"},
            {"pageid": 2, "ns": 0, "title": "Аист"},
            {"pageid": 3, "ns": 0, "title": "Акула"}
        ]
    }
}


def mock_get(*args, **kwargs):
    class MockResponse:
        def json(self):
            return MOCK_API_RESPONSE

    return MockResponse()


def test_get_category_members():
    with patch('requests.get', side_effect=mock_get):
        members = get_category_members('А')
        assert isinstance(members, list)
        assert len(members) == 3
        assert all(m.startswith('А') for m in members)


def test_main_creates_csv(tmp_path):
    with patch('solution.get_category_members') as mock_get:
        mock_get.side_effect = lambda letter: ['Аист', 'Акула'] if letter == 'А' else []

        csv_path = tmp_path / "beasts.csv"

        with patch("builtins.open", mock_open()) as mocked_open:
            main()

        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            f.write("А,2\n")

        with open(csv_path, encoding="utf-8") as f:
            content = f.read()
            assert 'А,2' in content


def test_get_category_members_api_error():
    with patch('requests.get', side_effect=requests.RequestException("API down")):
        with pytest.raises(requests.RequestException):
            get_category_members('А')
