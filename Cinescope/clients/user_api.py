from custom_requester.custom_requester import CustomRequester

from constants import USER_ENDPOINT


class UserAPI(CustomRequester):
    USER_BASE_URL = "https://auth.dev-cinescope.coconutqa.ru/"

    def __init__(self, session):
        self.session = session
        super().__init__(session, self.USER_BASE_URL)

    def get_user(self, user_locator,expected_status=200):
        return self.send_request("GET", f"user/{user_locator}",expected_status=expected_status)

    def create_user(self, registration_user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="user",
            json=registration_user_data.model_dump(mode="json",exclude_unset=True),
            expected_status=expected_status
        )
