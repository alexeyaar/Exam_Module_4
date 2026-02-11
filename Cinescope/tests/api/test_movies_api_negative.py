import pytest
from Cinescope.clients.api_manager import ApiManager
from Cinescope.constants import user_creds
@pytest.mark.negative
class TestMovieAPINegative:

    def test_get_movies_bad_filtered(self, api_manager: ApiManager, generate_random_int):
        # Получение списка афиш c ошибочной фильтрацией
        response = api_manager.movies_api.get_movies_info_filtered(expected_status=400,locations=generate_random_int)
        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"
        #assert response.text != generate_random_int, ""

    def test_create_movie_not_body(self,api_manager: ApiManager,):
        #Создание фильма без тела запроса
        api_manager.auth_api.authenticate(user_creds)
        response = api_manager.movies_api.create_movies(data={},expected_status=400)
        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"

    def test_get_bad_movie(self,api_manager: ApiManager,bad_id_movies,):
        #Получение несуществующего фильма
        response_get = api_manager.movies_api.get_bad_movie(bad_id_movies,expected_status=500)
        assert "message" in response_get.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "statusCode" in response_get.json(), "В теле ответа отсутствует статус код"

    def test_delete_bad_movie(self,api_manager:ApiManager,bad_id_movies):
        api_manager.auth_api.authenticate(user_creds)
        #Удаление фильма
        response = api_manager.movies_api.delete_bad_movie(bad_id_movies,expected_status=404)
        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"

    def test_edit_movie_not_body(self, create_movie, api_manager: ApiManager, data_for_edit_bad_movie):
        # Изменение фильма
        response = api_manager.movies_api.edit_movie_bad(data_for_edit_bad_movie,create_movie['id'],expected_status=400)
        assert "message" in response.json(), "В теле ответа отсутствует сообщение об ошибке"
        assert "statusCode" in response.json(), "В теле ответа отсутствует статус код"
        assert "error" in response.json(), "В теле ответа отсутствует описание ошибки"
