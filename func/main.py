from http import HTTPStatus

from etria_logger import Gladsheim

from src.domain.enums.status_code.enum import InternalCode
from src.domain.exceptions.exceptions import ErrorOnDecodeJwt, FailToFetchData, InternalServerError
from src.domain.models.jwt.response import Jwt
from src.domain.models.response.model import ResponseModel
from src.services.employ_type.service import EmployTypeService
import flask


async def get_employ_type() -> flask.Response:

    thebes_answer = flask.request.headers.get("x-thebes-answer")

    try:
        jwt_data = Jwt(jwt=thebes_answer)
        await jwt_data()
        service_response = EmployTypeService.get_employ_type_response()

        response = ResponseModel(
            success=True,
            code=InternalCode.SUCCESS.value,
            message="SUCCESS",
            result=service_response
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID.value,
            message="Error On Decoding JWT"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except TypeError as error:
        Gladsheim.error(error=error, message=str(error))
        response = ResponseModel(
            success=False,
            code=InternalCode.DATA_NOT_FOUND.value,
            message="Data not found or inconsistent"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except FailToFetchData as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR.value,
            message="Not able to get data from database"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except (Exception, InternalServerError) as error:
        Gladsheim.error(error=error, message=str(error))
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR.value,
            message="Something went wrong"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
