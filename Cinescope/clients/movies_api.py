from Exam_Module_4.Cinescope.constants import BASE_URL
from Exam_Module_4.Cinescope.custom_requester.custom_requester import MoviesRequester


class MoviesAPI(MoviesRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL)
        self.session = session

        """Класс для работы с API фильмов."""
    def get_movies_info(self):
        #Получение списка афиш
        return self.send_request(
            method="GET",
            endpoint="/movies",
            expected_status=200,

        )

    def get_movies_info_filtered(self,expected_status = 200,**kwargs):
        #Получение списка афиш c фильтрацией
        return self.send_request(
            method="GET",
            endpoint=f"/movies",
            expected_status=expected_status,
            params=kwargs

        )
    def create_movies(self,data = None,expected_status = 201):
        return self.send_request(
            method="POST",
            endpoint="/movies",
            expected_status=expected_status,
            data=data
        )
    def get_movie(self,create_movie,expected_status = 200):
        return self.send_request(
            method="GET",
            endpoint=f"/movies/{create_movie['id']}",
            expected_status=expected_status
        )
    def delete_movie(self,create_movie,expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"/movies/{create_movie['id']}",
            expected_status=expected_status        )

    def edit_movie(self,create_movie,data_for_edit_movie,expected_status = 200):
        return self.send_request(
            method="PATCH",
            endpoint=f"/movies/{create_movie}",
            data=data_for_edit_movie,
            expected_status = expected_status
        )
    def get_bad_movie(self,bad_id_movies,expected_status = 200):
        return self.send_request(
            method="GET",
            endpoint=f"/movies/{bad_id_movies}",
            expected_status=expected_status
        )

    def delete_bad_movie(self,bad_id_movies,expected_status = 400):
        return self.send_request(
            method="DELETE",
            endpoint=f"/movies/{bad_id_movies}",
            expected_status=expected_status
        )

    def edit_movie_bad(self,data_for_edit_bad_movie, create_movie,expected_status = 400):
        return self.send_request(
            method="PATCH",
            endpoint=f"/movies/{create_movie}",
            data=data_for_edit_bad_movie,
            expected_status=expected_status
        )