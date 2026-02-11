import pytest
from Cinescope.constants import LOGIN_ENDPOINT


@pytest.mark.negative
class TestNegativeAuth:
    def test_auth_no_password(self,test_user,requester):
     """Авторизация без пароля"""

     login_data = {
         "email":test_user["email"],
         "password": ""
     }
     response_auth = requester.send_request(
     method="POST",
     endpoint=LOGIN_ENDPOINT,
     data=login_data,
     expected_status=401
     )

    def test_auth_no_body(self,test_user,requester):
     """Авторизация без тела запроса """
     response_2auth = requester.send_request(
     method="POST",
     endpoint=LOGIN_ENDPOINT,
     data="",
      expected_status=400
     )
