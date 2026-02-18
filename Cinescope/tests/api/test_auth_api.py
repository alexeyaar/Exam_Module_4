import pytest
from Exam_Module_4.Cinescope.clients.api_manager import ApiManager
from Exam_Module_4.Cinescope.models.base_models import RegisterUserResponse


@pytest.mark.positive
class TestAuthAPI:

    def test_register_user(self, api_manager: ApiManager, test_user):
        response = api_manager.auth_api.register_user(user_data=test_user)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"

    def test_login_user(self, api_manager: ApiManager, registered_user):

        login_data = {
            "email": registered_user.email,
            "password": registered_user.password
        }
        response = api_manager.auth_api.login_user(login_data,expected_status=200)
        response_data = response.json()
        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user.email, "Email не совпадает"

"""    def test_del_user(self,api_manager: ApiManager,registered_user,):
        api_manager.auth_api.authenticate(user_creds)
        response = api_manager.user_api.delete_user(user_id = registered_user['id'] )
"""


@pytest.mark.negative
class TestNegativeAuth:
    def test_auth_no_password(self,test_user,requester,api_manager: ApiManager):
     """Авторизация без пароля"""
     api_manager.auth_api.register_user(test_user)
     login_data = {
         "email":test_user.email,
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
