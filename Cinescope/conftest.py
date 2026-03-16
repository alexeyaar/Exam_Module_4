from faker import Faker
import pytest
import requests
from sqlalchemy.orm import Session

from models.page_odjects_models import CinescopeRegisterPage
from db_reuester.db_client import get_db_session
from models.user_models import TestUser, RegisterUserResponse
from tests.api.test_user_api import TestUserApi
from entities.user import User
from resources.user_creds import SuperAdminCreds
from custom_requester.custom_requester import CustomRequester
from clients.api_manager import ApiManager
from utils.data_generator  import DataGenerator
from constants import user_creds, REGISTER_ENDPOINT, BASE_URL, Roles
from db_reuester.db_helpers import DBHelper
import pytest
from playwright.sync_api import sync_playwright

DEFAULT_UI_TIMEOUT = 60000
faker = Faker()


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
#         "roles": [Roles.USER.value]
#     }

@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value],
    )


@pytest.fixture(scope="function")
def registered_user(requester, test_user) -> RegisterUserResponse:
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user.model_dump(mode="json",exclude_unset=True),
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.model_dump(mode="json",exclude_unset=True)
    # registered_user.id = response_data["id"]
    return TestUser(**registered_user)

# @pytest.fixture(scope="function")
# def registered_user_ui(requester, test_user):
#
#     response = requester.send_request(
#         method="POST",
#         endpoint=REGISTER_ENDPOINT,
#         data=test_user,
#         expected_status=201
#     )
#     response_data = response.json()
#     registered_user = test_user.copy()
#     registered_user["id"] = response_data["id"]
#     return registered_user
@pytest.fixture
def registered_user_ui():
    with sync_playwright() as playwright:
        random_email = DataGenerator.generate_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_random_password()
        browser = playwright.chromium.launch()
        page = browser.new_page()

        # Создаем объект страницы регистрации cinescope
        register_page = CinescopeRegisterPage(page)
        user_creds = {
            'email':random_email,
            'password':random_password
        }

        # Открываем страницу
        register_page.open()
        register_page.register(random_name, random_email, random_password, random_password)
        return user_creds


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

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

# @pytest.fixture(scope="function")
# def creation_user_data(test_user):
#     updated_data = test_user.copy()
#     updated_data.update({
#         "verified": True,
#         "banned": False
#     })
#     return updated_data

@pytest.fixture
def common_user(user_session, super_admin, registration_user_data):
    new_session = user_session()

    common_user = User(
        registration_user_data.email,
        registration_user_data.password,
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(registration_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def common_admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_admin = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.ADMIN.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_admin.api.auth_api.authenticate(common_admin.creds)
    return common_admin

@pytest.fixture
def user_fixture(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def registration_user_data() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email= DataGenerator.generate_random_email(),
        fullName= DataGenerator.generate_random_name(),
        password= random_password,
        passwordRepeat= random_password,
        roles=[Roles.USER.value],
        banned= False,
        verified = True
    )
# def test_user() -> TestUser:
#     random_password = DataGenerator.generate_random_password()
#
#     return TestUser(
#         email=DataGenerator.generate_random_email(),
#         fullName=DataGenerator.generate_random_name(),
#         password=random_password,
#         passwordRepeat=random_password,
#         roles=[Roles.USER.value]
# def registration_user_data():
#     random_password = DataGenerator.generate_random_password()
#
#     return {
#         "email": DataGenerator.generate_random_email(),
#         "fullName": DataGenerator.generate_random_name(),
#         "password": random_password,
#         "passwordRepeat": random_password,
#         "roles": [Roles.USER.value],
#         "banned": False,
#         "virified": True
#     }

@pytest.fixture(scope="function")
def db_session():
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session):
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    user = db_helper.create_test_users(DataGenerator.generate_user_data())
    yield user
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)
@pytest.fixture
def data_movie_db():
    return DataGenerator.generate_movies_data()

@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch()
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True,snapshots=True,sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    context.close()
@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()
