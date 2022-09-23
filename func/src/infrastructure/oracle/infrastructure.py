# THIRD PART IMPORT
import cx_Oracle
from decouple import config


class OracleInfrastructure:
    @classmethod
    def get_connection(cls) -> cx_Oracle.Cursor:
        connection = cls._make_connection()
        return connection.cursor()

    @classmethod
    def _make_connection(cls) -> cx_Oracle.Connection:
        connection = cx_Oracle.connect(
            user=config("ORACLE_USER"),
            password=config("ORACLE_PASSWORD"),
            dsn=cx_Oracle.makedsn(
                config("ORACLE_BASE_DSN"),
                config("ORACLE_PORT"),
                service_name=config("ORACLE_SERVICE"),
            ),
            encoding=config("ORACLE_ENCODING"),
        )
        return connection
