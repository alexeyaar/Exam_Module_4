from constants import LOGIN_ENDPOINT, REGISTER_ENDPOINT,USER_ENDPOINT
from custom_requester.custom_requester import CustomRequester



class AuthAPI(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru")

    def register_user(self, user_data, expected_status=201):

        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            json=user_data.model_dump(mode="json",exclude_unset=True),
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status=201):

        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            json=login_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id):
        return self.send_request(
            method="DELETE",
            endpoint=f"{USER_ENDPOINT}/{user_id}",
            expected_status=200
        )




    def authenticate(self, user_creds):
        print("Креды:",user_creds, "+++++++++++++++++++++++++++++++++++++++++++")
        login_data = {
            "email": user_creds["email"],
            "password": user_creds["password"]
        }
        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("Токен отсутствует в ответе ")

        token = response["accessToken"]
        self._update_session_headers(**{"authorization": "Bearer " + token})