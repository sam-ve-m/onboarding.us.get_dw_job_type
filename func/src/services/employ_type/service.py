# PROJECT IMPORTS
from src.domain.models.employ_type.response.model import EmployTypeToResponse
from src.repositories.job_type.repository import EmployTypeRepository


class EmployTypeService:

    @classmethod
    def get_employ_type_response(cls) -> list:
        employ_type = EmployTypeRepository.get_employ_type()

        response = EmployTypeToResponse.employ_type_response(
            employ_type
        )

        return response
