import pytest

from Cinescope.clients.api_manager import ApiManager
from Cinescope.constants import LOGIN_ENDPOINT


@pytest.mark.negative
class TestNegativeAuth:
    def test_auth_no_password(self,test_user,requester,api_manager: ApiManager):
     """Авторизация без пароля"""
     api_manager.auth_api.register_user(test_user)
     login_data = {
         "email":test_user["email"],
         "password": ""
     }
     response = api_manager.auth_api.login_user(login_data,expected_status=401)
     assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
     assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"
     assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"

    def test_auth_no_body(self,test_user,requester,api_manager):
     """Авторизация без тела запроса """
     api_manager.auth_api.register_user(test_user)
     login_data = { }
     response = api_manager.auth_api.login_user(login_data, expected_status=401)
     assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
     assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"
     assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"
