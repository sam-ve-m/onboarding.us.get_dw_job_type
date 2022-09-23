# PROJECT IMPORTS
import logging.config
from http import HTTPStatus
from unittest.mock import MagicMock
from unittest.mock import patch

import flask
import pytest
from decouple import RepositoryEnv, Config

with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from main import get_employ_type
                from src.domain.models.jwt.response import Jwt
                from src.domain.enums.status_code.enum import InternalCode
                from src.domain.models.response.model import ResponseModel
                from src.domain.exceptions.exceptions import InternalServerError, ErrorOnDecodeJwt, FailToFetchData
                from src.services.employ_type.service import EmployTypeService


internal_server_error_case = (
    InternalServerError("dummy"),
    "dummy",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Something went wrong",
    HTTPStatus.INTERNAL_SERVER_ERROR
)
error_on_decode_jwt_case = (
    ErrorOnDecodeJwt(),
    ErrorOnDecodeJwt.msg,
    InternalCode.JWT_INVALID,
    "Error On Decoding JWT",
    HTTPStatus.UNAUTHORIZED
)
fail_to_fetch_data_case = (
    FailToFetchData(),
    FailToFetchData.msg,
    InternalCode.INTERNAL_SERVER_ERROR,
    "Not able to get data from database",
    HTTPStatus.INTERNAL_SERVER_ERROR
)


typeerror_exception_case = (
    TypeError("dummy"),
    "dummy",
    InternalCode.DATA_NOT_FOUND,
    "Data not found or inconsistent",
    HTTPStatus.UNAUTHORIZED
)
exception_case = (
    Exception("dummy"),
    "dummy",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Something went wrong",
    HTTPStatus.INTERNAL_SERVER_ERROR
)


@pytest.mark.asyncio
@pytest.mark.parametrize("exception,error_message,internal_status_code,response_message,response_status_code", [
    internal_server_error_case,
    error_on_decode_jwt_case,
    fail_to_fetch_data_case,
    typeerror_exception_case,
    exception_case,
])
@patch.object(EmployTypeService, "get_employ_type_response")
@patch.object(Gladsheim, "error")
@patch.object(Jwt, "__init__", return_value=None)
@patch.object(Jwt, "__call__")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response")
async def test_get_employ_type_raising_errors(
            mocked_build_response, mocked_response_instance, mocked_jwt_decode,
            mocked_jwt_instance, mocked_logger, mocked_service, monkeypatch,
            exception, error_message, internal_status_code, response_message, response_status_code,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    mocked_jwt_decode.side_effect = exception
    await get_employ_type()
    mocked_service.assert_not_called()
    mocked_logger.assert_called_once_with(error=exception, message=error_message)
    mocked_response_instance.assert_called_once_with(
        success=False,
        code=internal_status_code.value,
        message=response_message
    )
    mocked_build_response.assert_called_once_with(status=response_status_code)


dummy_response = "response"


@pytest.mark.asyncio
@patch.object(EmployTypeService, "get_employ_type_response", return_value=dummy_response)
@patch.object(Gladsheim, "error")
@patch.object(Jwt, "__init__", return_value=None)
@patch.object(Jwt, "__call__")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_response)
async def test_get_employ_type(
        mocked_build_response, mocked_response_instance, mocked_jwt_decode,
        mocked_jwt_instance, mocked_logger, mocked_service, monkeypatch,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    response = await get_employ_type()
    mocked_jwt_decode.assert_called()
    mocked_service.assert_called()
    mocked_logger.assert_not_called()
    mocked_response_instance.assert_called_once_with(
        result=dummy_response,
        success=True,
        code=InternalCode.SUCCESS.value,
        message='SUCCESS',
    )
    mocked_build_response.assert_called_once_with(status=HTTPStatus.OK)
    assert dummy_response == response
