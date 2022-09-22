# STANDARD IMPORTS
from typing import Union

# THIRD PART IMPORTS
from etria_logger import Gladsheim
from mnemosine import SyncCache


class EmployTypeCacheRepository:
    enum_key = "jormungandr:EnumEmployType"

    @classmethod
    def save_employ_type_enum(cls, employ_type: list, time: int = 3600) -> bool:
        try:
            SyncCache.save(cls.enum_key, list(employ_type), int(time))
            return True
        except ValueError as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False
        except TypeError as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False
        except Exception as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False

    @classmethod
    def get_employ_type_enum(cls) -> Union[list, None]:
        result = SyncCache.get(cls.enum_key)
        return result
