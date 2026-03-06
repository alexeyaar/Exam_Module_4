import pytest
from clients.api_manager import ApiManager

from models.user_models import RegisterUserResponse,LoginUserResponse,BadLogin


@pytest.mark.positive
class TestAuthAPI:
    # @pytest.mark.skip(reason="Пока пропустим")
    def test_register_user(self, api_manager: ApiManager, registration_user_data):
        response = api_manager.auth_api.register_user(registration_user_data)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == registration_user_data.email, "Email не совпадает"


    def test_login_user(self, api_manager: ApiManager, registered_user):

        login_data = {
            "email": registered_user.email,
            "password": registered_user.password
        }
        response = api_manager.auth_api.login_user(login_data,expected_status=201)
        response_data = response.json()
        login_response_user = LoginUserResponse(**response.json())
        # Проверки
        assert response_data["user"]["email"] == registered_user.email, "Email не совпадает"

    def test_delete_user(self,super_admin,registration_user_data):
        response = super_admin.api.user_api.create_user(registration_user_data)
        resp_json = response.json()
        super_admin.api.auth_api.delete_user(resp_json["id"])
        super_admin.api.user_api.get_user(resp_json["id"],expected_status=200)



@pytest.mark.negative
class TestNegativeAuth:
    # @pytest.mark.xfail
    def test_auth_no_password(self,registration_user_data,api_manager: ApiManager):
     api_manager.auth_api.register_user(registration_user_data)
     login_data = {
         "email":registration_user_data.email,
         "password": ""
     }
     response = api_manager.auth_api.login_user(login_data,expected_status=401)
     resp_bad_registration = BadLogin(**response.json())

     # assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
     # assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"
     # assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"

    def test_auth_no_body(self,registration_user_data,api_manager):
     """Авторизация без тела запроса """
     api_manager.auth_api.register_user(registration_user_data)
     login_data = { }
     response = api_manager.auth_api.login_user(login_data, expected_status=500)
     resp = BadLogin(**response.json())














     # assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
     # assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"
     # assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"




    # def test_register_user(self, api_manager: ApiManager, test_user):
    #     """
    #     Тест на регистрацию пользователя.
    #     """
    #     response = api_manager.auth_api.register_user(test_user)
    #     response_data = response.json()
    #
    #     # Проверки
    #     assert response_data["email"] == test_user["email"], "Email не совпадает"
    #     assert "id" in response_data, "ID пользователя отсутствует в ответе"
    #     assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
    #     assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    # @pytest.mark.skipif(x,reason ="что то не так")