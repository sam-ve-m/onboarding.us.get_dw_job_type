# STANDARD IMPORTS
from dataclasses import dataclass
from pydantic import BaseModel


class EmployTypeModel(BaseModel):
    code: str
    value: str


@dataclass(init=True)
class EmployTypeResponse:
    code: str
    description: str

    def __repr__(self):
        employ_response = {
            "code": self.code,
            "value": self.description
        }

        return employ_response
