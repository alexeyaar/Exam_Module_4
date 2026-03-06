from models.user_models import RegisterUserResponse
from clients.api_manager import ApiManager


class TestUserApi:

    def test_create_user(self, super_admin, registration_user_data):
        response = super_admin.api.user_api.create_user(registration_user_data).json()
        resp_check  = RegisterUserResponse(**response)

        assert response.get('verified') is True

    def test_get_user_by_locator(self, super_admin, registration_user_data):
        created_user_response = super_admin.api.user_api.create_user(registration_user_data).json()

        response_by_id = super_admin.api.user_api.get_user(created_user_response["id"])
        resp_id_check = RegisterUserResponse(**response_by_id.json())
        response_by_email = super_admin.api.user_api.get_user(created_user_response["email"])
        resp_email_check = RegisterUserResponse(**response_by_email.json())


        # assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        # assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        # assert response_by_id.get('email') == creation_user_data['email']
        # assert response_by_id.get('fullName') == creation_user_data['fullName']
        # assert response_by_id.get('roles', []) == creation_user_data['roles']
        # assert response_by_id.get('verified') is True

    def test_get_user_by_id_common_user(self,super_admin,api_manager: ApiManager,registration_user_data):
        responses = super_admin.api.user_api.create_user(registration_user_data).json()
        api_manager.user_api.get_user(responses['email'], expected_status=401)
