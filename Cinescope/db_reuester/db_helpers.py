from sqlalchemy.orm import Session
from db_models.user import UserDBModel
from db_models.movies import MoviesDBModel

class DBHelper:
    def __init__(self,db_session: Session):
        self.db_session = db_session

    def create_test_users(self,user_data:dict) -> UserDBModel:
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self,user_id:str):
        return self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    def get_user_by_email(self,user_email:str):
        return self.db_session.query(UserDBModel).filter(UserDBModel.email== user_email).first()

    def get_usre_by_name(self,name:str):
        return self.db_session.query(UserDBModel).filter(UserDBModel.full_name ==name).first()
    def user_exists_by_email(self,email:str):
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).count()>0
    def delete_user(self,user:UserDBModel):
        self.db_session.delete(user)
        self.db_session.commit()

    def cleanup_test_data(self,objects_to_delete:list):
        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

    def create_movie(self,data_movie):
        movie = MoviesDBModel(**data_movie)
        self.db_session.add(movie)
        self.db_session.commit()
        self.db_session.refresh(movie)
        return data_movie

    def get_movies_by_id(self,movie_id):
        return self.db_session.query(MoviesDBModel).filter(MoviesDBModel.id == movie_id).first()

    def get_movies_by_name(self,movie_name):
        return self.db_session.query(MoviesDBModel).filter(MoviesDBModel.name == movie_name).first()

