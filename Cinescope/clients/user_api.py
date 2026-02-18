from Exam_Module_4.Cinescope.custom_requester.custom_requester import CustomRequester
from Exam_Module_4.Cinescope.constants import BASE_URL

class UserAPI(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session,base_url=BASE_URL)
        self.session = session


    def delete_user(self, user_id, expected_status=204):

            return self.send_request(
                method="DELETE",
                endpoint=f"/users/{user_id}",
                expected_status=expected_status
            )
