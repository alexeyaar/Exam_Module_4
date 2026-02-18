import pytest
from Exam_Module_4.Cinescope.clients.api_manager import ApiManager
from Exam_Module_4.Cinescope.conftest import common_admin
from Exam_Module_4.Cinescope.constants import user_creds
@pytest.mark.positive
class TestMoviesAPI:

    def test_get_movies(self, common_user,api_manager: ApiManager):
        #Получение списка афиш
        response = common_user.api.movies_api.get_movies_info()

        assert "movies" in response.json(), "В теле ответа отсутствует список фильмов"

    def test_get_movies_filtered(self, api_manager: ApiManager, generate_random_int,common_user):
        # Получение списка афиш c фильтрацией
        response = common_user.api.movies_api.get_movies_info_filtered(page=generate_random_int)

        assert response.json()['page'] == generate_random_int, "Неверная фильтрация страницы"

    @pytest.mark.parametrize("minPrice,genreId,locations", [(1, 1, "MSK"), (100, 15, "SPB"), (900, 900, "MSK")])
    def test_get_movies_filtered(self, api_manager: ApiManager, common_user, minPrice, genreId, locations):
        # Получение списка афиш c фильтрацией
        response = common_user.api.movies_api.get_movies_info_filtered(expected_status=200, minPrice=minPrice,
                                                                       genreId=genreId, locations=locations)
    def test_create_movie(self,data_movie,api_manager: ApiManager,common_admin):
        #Создание фильма
        common_admin.api.auth_api.authenticate(user_creds)
        response = common_admin.api.movies_api.create_movies(data_movie)
        #Проверяем создание фильма
        common_admin.api.movies_api.get_movie(response.json())

        assert response.json()['name'] == data_movie["name"], "Некорректное заполнение поля name"
        assert response.json()['location'] == data_movie["location"], "Некорректное заполнение поля location"
        assert response.json()['price'] == data_movie["price"], "Некорректное заполнение поля price"
        assert response.json()['description'] == data_movie["description"], "Некорректное заполнение поля description"
        assert response.json()['imageUrl'] == data_movie["imageUrl"], "Некорректное заполнение поля imageUrl"
        assert response.json()['published'] == data_movie["published"], "Некорректное заполнение поля published"
        assert response.json()['genreId'] == data_movie["genreId"], "Некорректное заполнение поля genreId"

    def test_create_movie_by_user_role(self, data_movie, api_manager: ApiManager, common_user, ):
        # Создание фильма
        response = common_user.api.movies_api.create_movies(data_movie, expected_status=403)
        # Проверяем создание фильма
        # common_user.api.movies_api.get_movie(response.json())

        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"

    def test_get_movie(self,api_manager: ApiManager,create_movie,common_user):
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



    def test_delete_movie(self,api_manager:ApiManager,create_movie,super_admin):
        #Удаление фильма

        super_admin.api.movies_api.delete_movie(create_movie)
        get_response = super_admin.api.movies_api.get_movie(create_movie,expected_status=404)


        assert get_response.json()['message'] == "Фильм не найден", "Отсутствует информационное сообщение"



    def test_edit_movie(self,create_movie,api_manager: ApiManager,data_for_edit_movie,super_admin):
        # Изменение фильма
        response = super_admin.api.movies_api.edit_movie(create_movie['id'],data_for_edit_movie)
        response_get = super_admin.api.movies_api.get_movie(create_movie)

        assert response_get.json()['name'] == data_for_edit_movie["name"], f"Не заменено поля name: {response_get.json()['name']}"
        assert response_get.json()['imageUrl'] == data_for_edit_movie["imageUrl"], "Не заменено поля imageUrl"
        assert response_get.json()['price'] == data_for_edit_movie['price'],"Не заменено поля price"
        assert response_get.json()['id'] == create_movie['id'], "Изменено поле id!"
        assert response_get.json()["description"] == response.json().get("description"), "Изменено поле description"
        assert response_get.json()["published"] == response.json().get("published"), "Изменено поле published"
        assert response_get.json()["location"] == response.json().get("location"), "Изменено поле location"
        assert response_get.json()["rating"] == response.json().get("rating"), "Изменено поле rating"
        assert response_get.json()["genreId"] == response.json().get("genreId"), "Изменено поле genreId"
        assert response_get.json()["createdAt"] == response.json().get("createdAt"), "Изменено поле createdAt"
        assert response_get.json()["genre"]["name"] == response.json()["genre"]['name'], "Изменен жанр"



    @pytest.mark.parametrize("create_movie",[({"id":"666"}),({"id":12}),({"id":123123123}),({"id":4556434534})])
    def test_delete_movie_parms(self,api_manager:ApiManager,create_movie,super_admin,expected_status = 404):
        #Удаление фильма

        super_admin.api.movies_api.delete_movie(create_movie,expected_status =expected_status)
        #get_response = super_admin.api.movies_api.get_movie(create_movie)


    # assert get_response.json()['message'] == "Фильм не найден", "Отсутствует информационное сообщение"


@pytest.mark.negative
class TestMovieAPINegative:

    @pytest.mark.parametrize("minPrice,genreId,locations",[("A",500,"MSK"),(500,"B","SPB"),(10,122,"MRSK")], ids=["inValid minPrice","Invalid genreId","Invalid locations"])
    def test_get_movies_filtered(self, api_manager: ApiManager,common_user,minPrice,genreId,locations):
        # Получение списка афиш c фильтрацией
        response = common_user.api.movies_api.get_movies_info_filtered(expected_status=400,minPrice=minPrice,genreId=genreId,locations=locations)

        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"

    def test_create_movie_not_body(self,api_manager: ApiManager,super_admin):
        #Создание фильма без тела запроса
        super_admin.api.auth_api.authenticate(user_creds)
        response = super_admin.api.movies_api.create_movies(data={},expected_status=400)

        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"

    def test_get_bad_movie(self,api_manager: ApiManager,bad_id_movies,common_user):
        #Получение несуществующего фильма
        response_get = common_user.api.movies_api.get_bad_movie(bad_id_movies,expected_status=500)

        assert "message" in response_get.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "statusCode" in response_get.json(), "В теле ответа отсутствует статус код"

    def test_delete_bad_movie(self,api_manager:ApiManager,bad_id_movies,super_admin):
        super_admin.api.auth_api.authenticate(user_creds)
        #Удаление фильма
        response = super_admin.api.movies_api.delete_bad_movie(bad_id_movies,expected_status=404)

        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"

    def test_edit_movie_not_body(self, create_movie, api_manager: ApiManager, data_for_edit_bad_movie,super_admin):
        # Изменение фильма
        response = super_admin.api.movies_api.edit_movie_bad(data_for_edit_bad_movie,create_movie['id'],expected_status=400)

        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"



