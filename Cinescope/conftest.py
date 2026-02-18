import sys
from pathlib import Path
import os
from Exam_Module_4.Cinescope.models.base_models import TestUser
from faker import Faker
import pytest
import requests
from Exam_Module_4.Cinescope.entities.user import User
from custom_requester.custom_requester import CustomRequester
from Exam_Module_4.Cinescope.clients.api_manager import ApiManager
from Exam_Module_4.Cinescope.utils.data_generator  import DataGenerator
from Exam_Module_4.Cinescope.constants import user_creds, REGISTER_ENDPOINT, BASE_URL, Roles
from Exam_Module_4.Cinescope.resources.user_creds import SuperAdminCreds

THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parent.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))




faker = Faker('ru_RU')


# @pytest.fixture(scope="function",autouse=False)
# def test_user():
#     """
#     Генерация случайного пользователя для тестов.
#     """
#     random_email = DataGenerator.generate_random_email()
#     random_name = DataGenerator.generate_random_name()
#     random_password = DataGenerator.generate_random_password()
#
#     return {
#         "email": random_email,
#         "fullName": random_name,
#         "password": random_password,
#         "passwordRepeat": random_password,
#         "roles": Roles.USER.value
#     }

@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()
    print("Вызов фикстуры регистрации")

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope="function")
def registered_user(requester, test_user) -> TestUser:
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    print('Вызов фикстуры регистрации и данных зарегистрированного пользователя для логина')
    return TestUser(
        email=test_user.email,
        fullName=test_user.fullName,
        password=test_user.password,
        passwordRepeat=test_user.passwordRepeat,
        roles=test_user.roles
    )

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    http_session.base_url = BASE_URL
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)
@pytest.fixture
def generate_random_int():

    nums = faker.random_int(min=1, max = 50)
    return nums
@pytest.fixture
def data_movie():
    cities = ["MSK", "SPB"]

    return {
             "name": faker.catch_phrase(),
             "imageUrl":faker.image_url(),
             "price": faker.random_int(),
             "description": faker.paragraph(),
             "location": faker.random_element(cities),
             "published": faker.pybool(),
             "genreId": faker.random_int(min=1, max=10)
     }

@pytest.fixture
def create_movie(api_manager,data_movie):
    api_manager.auth_api.authenticate(user_creds)
    response = api_manager.movies_api.create_movies(data_movie)
    movie = response.json()

    return movie

@pytest.fixture
def data_for_edit_movie():
    return {
        "name": faker.catch_phrase(),
        "imageUrl": faker.image_url(),
        "price": faker.random_int()
    }
@pytest.fixture
def bad_id_movies():
    value = ["айди", True, False, None, [], {"cinema": 43}, (1,2,), "id"]
    return  faker.random_element(value)
@pytest.fixture
def data_for_edit_bad_movie():
    return {
        "name": faker.pybool(),
        "imageUrl": faker.random_int(),
        "price": faker.image_url()
    }
@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
            user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()
    super_admin = User(SuperAdminCreds.USERNAME,
                       SuperAdminCreds.PASSWORD,
                       [Roles.SUPER_ADMIN.value],
                       new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin
@pytest.fixture
def creation_user_data(test_user) -> TestUser:
    return TestUser(
        email=test_user.email,
        fullName=test_user.fullName,
        password=test_user.password,
        passwordRepeat=test_user.passwordRepeat,
        roles=test_user.roles,
        verified=True,
        banned= False
    )

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        list(Roles.USER.value),
        new_session)

    super_admin.api.admin_users_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def common_admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_admin = User(
        creation_user_data.email,
        creation_user_data.password,
        list(Roles.ADMIN.value),
        new_session)

    super_admin.api.admin_users_api.create_user(creation_user_data)
    common_admin.api.auth_api.authenticate(common_admin.creds)
    return common_admin
