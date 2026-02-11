from faker import Faker
import pytest
import requests
from custom_requester.custom_requester import CustomRequester
from Cinescope.clients.api_manager import ApiManager
from Cinescope.utils.data_generator  import DataGenerator
from Cinescope.constants import user_creds, REGISTER_ENDPOINT, BASE_URL

faker = Faker('ru_RU')


@pytest.fixture(scope="function",autouse=False)
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="function")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

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
    resp_autentificate = api_manager.auth_api.authenticate(user_creds)
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