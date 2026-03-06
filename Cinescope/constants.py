from enum import Enum

BASE_URL = "https://auth.dev-cinescope.coconutqa.ru/"
API_URL = "https://api.dev-cinescope.coconutqa.ru"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
USER_ENDPOINT ="/user"


user_creds = {
    "email": "api1@gmail.com",
    "password": "asdqwe123Q"
}
class Roles(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"