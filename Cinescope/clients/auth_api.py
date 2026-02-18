from Exam_Module_4.Cinescope.constants import LOGIN_ENDPOINT, REGISTER_ENDPOINT
from Exam_Module_4.Cinescope.custom_requester.custom_requester import CustomRequester



class AuthAPI(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru")

    def register_user(self, user_data, expected_status=201):

        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status=200):

        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def delete_user(self):
        pass


    def authenticate(self, user_creds):
        if type(user_creds) == dict:
            login_data = {
            "email": user_creds["username"],
            "password": user_creds["password"]
            }
        else:
            login_data = {
                "email": user_creds[0],
                "password": user_creds[1]
        }
        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("Токен отсутствует в ответе ")

        token = response["accessToken"]
        self._update_session_headers(**{"authorization": "Bearer " + token})