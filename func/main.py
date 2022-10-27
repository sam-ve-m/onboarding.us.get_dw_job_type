from http import HTTPStatus

from etria_logger import Gladsheim

from src.domain.enums.status_code.enum import InternalCode
from src.domain.exceptions.exceptions import FailToFetchData
from src.domain.models.response.model import ResponseModel
from src.services.employ_type.service import EmployTypeService
import flask


async def get_employ_type() -> flask.Response:
    try:
        service_response = EmployTypeService.get_employ_type_response()
        response = ResponseModel(
            success=True,
            code=InternalCode.SUCCESS,
            message="SUCCESS",
            result=service_response
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except FailToFetchData as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Not able to get or save data in database"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except Exception as error:
        Gladsheim.error(error=error, message=str(error))
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Something went wrong"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
