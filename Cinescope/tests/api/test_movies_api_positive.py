import pytest
from Cinescope.clients.api_manager import ApiManager
from Cinescope.constants import user_creds
@pytest.mark.positive
class TestMoviesAPI:

    def test_get_movies(self,api_manager: ApiManager):
        #Получение списка афиш
        response = api_manager.movies_api.get_movies_info()
        assert "movies" in response.json(), "В теле ответа отсутствует список фильмов"

    def test_get_movies_filtered(self, api_manager: ApiManager, generate_random_int):
        # Получение списка афиш c фильтрацией
        response = api_manager.movies_api.get_movies_info_filtered(page=generate_random_int)
        assert response.json()['page'] == generate_random_int, "Неверная фильтрация страницы"

    def test_create_movie(self,data_movie,api_manager: ApiManager,):
        #Создание фильма
        api_manager.auth_api.authenticate(user_creds)
        response = api_manager.movies_api.create_movies(data_movie)
        #Проверяем создание фильма
        api_manager.movies_api.get_movie(response.json())

        assert response.json()['name'] == data_movie["name"], "Некорректное заполнение поля name"
        assert response.json()['location'] == data_movie["location"], "Некорректное заполнение поля location"
        assert response.json()['price'] == data_movie["price"], "Некорректное заполнение поля price"
        assert response.json()['description'] == data_movie["description"], "Некорректное заполнение поля description"
        assert response.json()['imageUrl'] == data_movie["imageUrl"], "Некорректное заполнение поля imageUrl"
        assert response.json()['published'] == data_movie["published"], "Некорректное заполнение поля published"
        assert response.json()['genreId'] == data_movie["genreId"], "Некорректное заполнение поля genreId"


    def test_get_movie(self,api_manager: ApiManager,create_movie):
        #Получение фильма
        response_get = api_manager.movies_api.get_movie(create_movie)
        assert response_get.json()["id"] == create_movie['id'], "Получен не запрашиваемый ресурс"
        assert response_get.json()["name"] == create_movie["name"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["price"] == create_movie["price"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["description"] == create_movie["description"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["imageUrl"] == create_movie["imageUrl"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["location"] == create_movie["location"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["published"] == create_movie["published"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["rating"] == create_movie["rating"], "Получен не запрашиваемый ресурс"
        assert response_get.json()["genreId"] == create_movie["genreId"], "Получен не запрашиваемый ресурс"

    def test_delete_movie(self,api_manager:ApiManager,create_movie):
        #Удаление фильма
        api_manager.movies_api.delete_movie(create_movie)
        get_response = api_manager.movies_api.get_movie(create_movie,expected_status=404)

        assert get_response.json()['message'] == "Фильм не найден", "Отсутствует информационное сообщение"



    def test_edit_movie(self,create_movie,api_manager: ApiManager,data_for_edit_movie):
        # Изменение фильма
        response = api_manager.movies_api.edit_movie(create_movie['id'],data_for_edit_movie)
        response_get = api_manager.movies_api.get_movie(create_movie)

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





