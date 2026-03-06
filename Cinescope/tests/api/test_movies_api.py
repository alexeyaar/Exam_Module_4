import pytest
from clients.api_manager import ApiManager
from constants import user_creds
import allure
import pytest_check as check
#pytestmark = pytest.mark.skip(reason="TASK-1234: Тесты временно отключены из-за нестабильности")


@pytest.mark.positive
class TestMoviesAPI:
    @pytest.mark.slow
    def test_get_movies(self,common_user):
        #Получение списка афиш
        response =common_user.api.movies_api.get_movies_info()

        assert "movies" in response.json(), "В теле ответа отсутствует список фильмов"

    @pytest.mark.regression
    def test_get_movies_filtered(self, generate_random_int, common_user):
        # Получение списка афиш c фильтрацией
        response = common_user.api.movies_api.get_movies_info_filtered(page=generate_random_int)

        assert response.json()['page'] == generate_random_int, "Неверная фильтрация страницы"

    @pytest.mark.parametrize(
        "minPrice, genreId, location",
        [
            pytest.param(1, 1, "MSK", id="мин.цена 1 + жанр 1 в Москве"),
            pytest.param(100, 15, "SPB", id="мин.цена 100 + жанр 15 в Питере"),
            pytest.param(900, 900, "MSK", id="мин.цена 900 + жанр 900 в Москве"),
        ]
    )

    @pytest.mark.api
    @pytest.mark.slow
    def test_get_movies_filtered_param(self, common_user,minPrice,genreId, location):
        # Получение списка афиш c фильтрацией
        response = common_user.api.movies_api.get_movies_info_filtered(minPrice=minPrice,location=location,genreId = genreId)

        # assert response.json()['page'] == generate_random_int, "Неверная фильтрация страницы"
    @pytest.mark.ui
    def test_create_movie(self,data_movie,super_admin):
        #Создание фильма

        response = super_admin.api.movies_api.create_movies(data_movie)
        #Проверяем создание фильма
        super_admin.api.movies_api.get_movie(response.json())

        assert response.json()['name'] == data_movie["name"], "Некорректное заполнение поля name"
        assert response.json()['location'] == data_movie["location"], "Некорректное заполнение поля location"
        assert response.json()['price'] == data_movie["price"], "Некорректное заполнение поля price"
        assert response.json()['description'] == data_movie["description"], "Некорректное заполнение поля description"
        assert response.json()['imageUrl'] == data_movie["imageUrl"], "Некорректное заполнение поля imageUrl"
        assert response.json()['published'] == data_movie["published"], "Некорректное заполнение поля published"
        assert response.json()['genreId'] == data_movie["genreId"], "Некорректное заполнение поля genreId"

    @pytest.mark.db
    def test_create_movie_by_user_role(self, data_movie, common_user):
        # Создание фильма

        response = common_user.api.movies_api.create_movies(data_movie,expected_status=403)

        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"


    def test_get_movie(self,create_movie,common_user):
        #Получение фильма
        response_get = common_user.api.movies_api.get_movie(create_movie)

        assert response_get.json()["id"] == create_movie['id'], "Получен не запрашиваемый ресурс"
        assert response_get.json()["name"] == create_movie["name"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["price"] == create_movie["price"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["description"] == create_movie["description"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["imageUrl"] == create_movie["imageUrl"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["location"] == create_movie["location"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["published"] == create_movie["published"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["rating"] == create_movie["rating"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["genreId"] == create_movie["genreId"], "Получен не запрашиваемый ресурс"

    @pytest.mark.flaky(reruns=3)
    @pytest.mark.slow
    @pytest.mark.parametrize("user_fixture,delete_status,get_status",[
                                 pytest.param("common_user",403,200, id="Обычный пользователь, без права удаления фильма"),
                                 pytest.param("super_admin",200,404, id="Cупер админ с правом удалять фильмы")],
                             indirect=["user_fixture"]
                             )

    def test_delete_movie(self,create_movie,user_fixture,delete_status,get_status):
        #Удаление фильма
        user_fixture.api.movies_api.delete_movie(create_movie,expected_status=delete_status)
        get_response = user_fixture.api.movies_api.get_movie(create_movie,expected_status=get_status)

        if delete_status == 403:
            assert get_response.json().get("id") == create_movie['id']
        else:
           assert get_response.json().get('message') == "Фильм не найден", "Отсутствует информационное сообщение"

    @allure.title("Тест редактирования афиши фильма ")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "AlexyA")
    def test_edit_movie(self,create_movie,data_for_edit_movie,super_admin):
        with allure.step(f" Изменяем созданный фильм c названием: {create_movie['name']}"):
            response = super_admin.api.movies_api.edit_movie(create_movie['id'],data_for_edit_movie)
        with allure.step("отправляем запрос на получение обновленного фильма "):
            response_get = super_admin.api.movies_api.get_movie(create_movie)

        with allure.step("Проверяем, что ответ соответствует ожидаемому"):
            with allure.step("Проверка нужные поля изменились, остальные остались не тронутыми"):  # обратите внимание на вложенность allure.step
                with check.check():
                        check.equal( response_get.json()['name'],data_for_edit_movie["name"], f"Не заменено поля name: {response_get.json()['name']}")
                        check.equal( response_get.json()['imageUrl'] ,data_for_edit_movie["imageUrl"], "Не заменено поля imageUrl")
                        check.equal( response_get.json()['price'] , data_for_edit_movie['price'],"Не заменено поля price")
                        check.equal( response_get.json()['id'] , create_movie['id'], "Изменено поле id!")
                        check.equal( response_get.json()["description"] , response.json().get("description"), "Изменено поле description")
                        check.equal( response_get.json()["published"] , response.json().get("published"), "Изменено поле published")
                        check.equal( response_get.json()["location"] , response.json().get("location"), "Изменено поле location")
                        check.equal( response_get.json()["rating"] , response.json().get("rating"), "Изменено поле rating")
                        check.equal( response_get.json()["genreId"] , response.json().get("genreId"), "Изменено поле genreId")
                        check.equal( response_get.json()["createdAt"] , response.json().get("createdAt"), "Изменено поле createdAt")
                        check.equal( response_get.json()["genre"]["name"] ,response.json()["genre"]['name'], "Изменен жанр")


    def test_get_movie_by_admin(self, create_movie, super_admin):
        # Получение фильма
        response_get = super_admin.api.movies_api.get_movie(create_movie)

@pytest.mark.negative
class TestMovieAPINegative:
    @pytest.mark.slow
    def test_get_movies_bad_filtered(self, generate_random_int,common_user):
        # Получение списка афиш c ошибочной фильтрацией
        response = common_user.api.movies_api.get_movies_info_filtered(expected_status=400,locations=generate_random_int)

        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"
        #assert response.text != generate_random_int, ""
    @pytest.mark.slow
    def test_create_movie_not_body(self,super_admin):
        #Создание фильма без тела запроса
        # super_admin.api.auth_api.authenticate(user_creds)
        response = super_admin.api.movies_api.create_movies(data={},expected_status=400)

        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"

    def test_get_bad_movie(self,bad_id_movies,super_admin):
        #Получение несуществующего фильма
        response_get = super_admin.api.movies_api.get_bad_movie(bad_id_movies,expected_status=500)

        assert "message" in response_get.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "statusCode" in response_get.json(), "В теле ответа отсутствует статус код"

    def test_delete_bad_movie(self, bad_id_movies,super_admin):

        #Удаление фильма
        response = super_admin.api.movies_api.delete_bad_movie(bad_id_movies,expected_status=404)

        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"

    def test_edit_movie_not_body(self, create_movie,super_admin, data_for_edit_bad_movie):
        # Изменение фильма
        response = super_admin.api.movies_api.edit_movie_bad(data_for_edit_bad_movie,create_movie['id'],expected_status=400)

        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"



