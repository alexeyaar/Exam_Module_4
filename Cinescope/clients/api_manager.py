from Exam_Module_4.Cinescope.clients.auth_api import AuthAPI
from Exam_Module_4.Cinescope.clients.user_api import UserAPI
from Exam_Module_4.Cinescope.clients.movies_api import MoviesAPI
from Exam_Module_4.Cinescope.clients.admin_users_api import AdminUsersApi

class ApiManager:
    def __init__(self, session):

        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.movies_api = MoviesAPI(session)
        self.admin_users_api = AdminUsersApi(session)

    def close_session(self):
        self.session.close()
