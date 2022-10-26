from typing import List
from unittest.mock import patch, MagicMock

from src.infrastructure.oracle.infrastructure import OracleInfrastructure
from src.repositories.oracle.repository import EmployTypeOracleRepository


@patch.object(EmployTypeOracleRepository, "_query")
def test_get_employ_type(mocked_query):
    response = EmployTypeOracleRepository.get_employ_type()
    mocked_query.assert_called_once()
    assert response == mocked_query.return_value


dummy_value = MagicMock()


@patch.object(EmployTypeOracleRepository, "_normalize_encode")
@patch.object(OracleInfrastructure, "get_cursor")
def test_query(mocked_infra, mocked_parser):
    result = EmployTypeOracleRepository._query(dummy_value)
    mocked_infra.assert_called_once_with()
    mocked_infra.return_value.__enter__.return_value.execute.assert_called_once_with(
        dummy_value
    )
    mocked_parser.assert_called_once_with(
        rows=mocked_infra.return_value.__enter__.return_value.fetchall.return_value
    )
    assert result == mocked_parser.return_value


def test_normalize_encode():
    result = EmployTypeOracleRepository._normalize_encode([
        (1, 1, 1),
        (1, 'お可愛いこと', 1),
    ])
    assert result == [
        (1, 1, 1),
        (1, 'お可愛いこと', 1),
    ]
