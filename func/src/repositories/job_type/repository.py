# STANDARD IMPORTS
from typing import List

# THIRD PART IMPORT
from etria_logger import Gladsheim

# PROJECT IMPORTS
from src.domain.exceptions.exceptions import FailToFetchData
from src.domain.models.employ_type.model import EmployTypeResponse
from src.repositories.base_repository.oracle.base import OracleBaseRepository
from src.repositories.cache.repository import EmployTypeCacheRepository


class EmployTypeRepository:

    @staticmethod
    def build_employ_type_model(employ_position: tuple) -> EmployTypeResponse:
        employ_type_model = EmployTypeResponse(
            code=employ_position[0],
            description=employ_position[1],
        )

        return employ_type_model

    @classmethod
    def get_employ_type(cls) -> List[EmployTypeResponse]:
        try:
            sql = """
                SELECT CODE, DESCRIPTION
                FROM USPIXDB001.SINCAD_EXTERNAL_EMPLOY_TYPES
                """

            employ_type_tuple = cls._get_employ_cached_enum(query=sql)

            employ_type_model = [
                EmployTypeRepository.build_employ_type_model(
                    employ_position=employ_position
                )
                for employ_position in employ_type_tuple
            ]
            return employ_type_model

        except Exception as error:
            Gladsheim.error(message=f"{cls.__class__}::get_employ_type", error=error)
            raise FailToFetchData()

    @classmethod
    def _get_employ_cached_enum(cls, query: str) -> list:
        if cached_enum := EmployTypeCacheRepository.get_employ_type_enum():
            return cached_enum

        enum_values = OracleBaseRepository.query(sql=query)
        EmployTypeCacheRepository.save_employ_type_enum(enum_values)
        return enum_values
