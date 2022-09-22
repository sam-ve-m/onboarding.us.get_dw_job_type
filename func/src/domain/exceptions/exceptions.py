class InternalServerError(Exception):
    pass


class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::decode_jwt_and_get_unique_id::Fail when trying to get unique_id," \
          " jwt not decoded successfully"


class FailToFetchData(Exception):
    msg = "Impossible to reach database and get data."
