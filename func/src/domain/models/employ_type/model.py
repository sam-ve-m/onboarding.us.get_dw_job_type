from pydantic import BaseModel


class EmployTypeModel(BaseModel):
    code: str
    value: str

    @classmethod
    def from_database(cls, database_return: tuple):
        model = cls(
            code=database_return[0],
            description=database_return[1],
        )
        return model
