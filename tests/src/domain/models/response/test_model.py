from unittest.mock import patch, MagicMock
from src.domain.models.response.model import ResponseModel


dummy_value = MagicMock()


@patch.object(ResponseModel, "to_dumps")
def test_instance(mocked_dumps):
    model = ResponseModel(dummy_value, dummy_value)
    assert model.result is None
    assert model.message is None

