import cx_Oracle
import pytest
from etria_logger import Gladsheim

from src.domain.exceptions.exceptions import FailToFetchData
from src.infrastructure.oracle.infrastructure import OracleInfrastructure
from unittest.mock import patch, MagicMock
from decouple import AutoConfig


dummy_env = "dummy env"


@patch.object(cx_Oracle, "makedsn")
@patch.object(cx_Oracle, "connect")
@patch.object(AutoConfig, "__call__")
def test_get_client(mocked_env, mocked_connection, mocked_dsn):
    new_connection_created = OracleInfrastructure._get_connection()
    assert new_connection_created == mocked_connection.return_value
    mocked_connection.assert_called_once_with(
        encoding=mocked_env.return_value,
        password=mocked_env.return_value,
        user=mocked_env.return_value,
        dsn=mocked_dsn.return_value,
    )
    mocked_dsn.assert_called_once_with(
        mocked_env.return_value,
        mocked_env.return_value,
        service_name=mocked_env.return_value,
    )
    reused_client = OracleInfrastructure._get_connection()
    assert reused_client == new_connection_created
    mocked_connection.assert_called_once_with(
        encoding=mocked_env.return_value,
        password=mocked_env.return_value,
        user=mocked_env.return_value,
        dsn=mocked_dsn.return_value,
    )
    mocked_dsn.assert_called_once_with(
        mocked_env.return_value,
        mocked_env.return_value,
        service_name=mocked_env.return_value,
    )
    OracleInfrastructure.connection = None


@patch.object(OracleInfrastructure, "_get_connection")
@patch.object(Gladsheim, "error")
def test_get_cursor(mocked_logger, mocked_connection):
    with pytest.raises(FailToFetchData):
        with OracleInfrastructure.get_cursor():
            raise cx_Oracle.DatabaseError(MagicMock())
    mocked_logger.assert_called_once()
