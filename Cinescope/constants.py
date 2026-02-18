from enum import Enum
BASE_URL = "https://auth.dev-cinescope.coconutqa.ru/"
API_URL = "https://api.dev-cinescope.coconutqa.ru"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"


user_creds = {
    "username": "api1@gmail.com",
    "password": "asdqwe123Q"
}
class Roles(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"