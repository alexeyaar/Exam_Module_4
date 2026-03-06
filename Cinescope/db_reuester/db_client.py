from resources.db_creds import DbCreds
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker




engine = create_engine(f"postgresql+psycopg2://{DbCreds.user}:{DbCreds.password}@{DbCreds.host}:{DbCreds.port}/{DbCreds.db_name}",echo=True)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db_session():
    return SessionLocal()


#
# def sdl_alchemy_SQL():
#     query = """
#     SELECT id, email, full_name, "password", created_at, updated_at, verified, banned, roles
#     FROM public.users
#     WHERE id = :user_id;
#     """
#
#     # Параметры запроса для подстановки в наш SQL запрос
#     user_id = "3a172562-e05d-4768-82dd-a098d8e7bbb3"
#
#     # Выполняем запрос
#     with engine.connect() as connection:  # выполняем соединенеи с базой данных и автоматически закрываем его по завершени выполнения
#         result = connection.execute(text(query), {"user_id": user_id})
#         for row in result:
#             print(row)
#
#
#
#
# #Modul_4\Cinescope\db_requester\sql_alchemy_client_simple_example.py
#
# def sdl_alchemy_ORM():
#     # Базовый класс для моделей
#     Base = declarative_base()
#
#     # Модель таблицы users
#     class User(Base):
#         __tablename__ = 'users'
#         id = Column(String, primary_key=True)
#         email = Column(String)
#         full_name = Column(String)
#         password = Column(String)
#         created_at = Column(DateTime)
#         updated_at = Column(DateTime)
#         verified = Column(Boolean)
#         banned = Column(Boolean)
#         roles = Column(String)
#
#     # Создаем сессию
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     user_id = "87671364-268e-4ee1-86a3-8f5878b1b2e2"
#
#     # Выполняем запрос
#     user = session.query(User).filter(User.id == user_id).first()
#
#     # Выводим результат (у нас в руках уже не строка а обьект!)
#     if user:
#         print(f"ID: {user.id}")
#         print(f"Email: {user.email}")
#         print(f"Full Name: {user.full_name}")
#         print(f"Password: {user.password}")
#         print(f"Created At: {user.created_at}")
#         print(f"Updated At: {user.updated_at}")
#         print(f"Verified: {user.verified}")
#         print(f"Banned: {user.banned}")
#         print(f"Roles: {user.roles}")
#     else:
#         print("Пользователь не найден.")
#
# if __name__ == "__main__":
#     sdl_alchemy_ORM()

# def create_connection_db():
#     connection = psycopg2.connect(
#         dbname = DbCreds.db_name,
#         user =DbCreds.user,
#         password = DbCreds.password,
#         host = DbCreds.host,
#         port = DbCreds.port
#
#     )
#     cursor = connection.cursor()
#     cursor.execute("SELECT id, full_name FROM users")
#
#     # Получение пакета из 5 строк
#     cursor.execute('''
#                DELETE from genres
#                where id = %s;
#            ''', ('31',))
#     affected_rows = cursor.rowcount
#     print(f"Количество обновленных строк: {affected_rows}")
#
#     connection.commit()
    # cursor.execute("SELECT id, email, full_name, created_at, updated_at, verified, banned, roles FROM public.users")
    # print(cursor.fetchone())

    # cursor_factory =connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # cursor_factory.execute("SELECT id, email, full_name, created_at, updated_at, verified, banned, roles FROM public.users WHERE id='d7864515-04d8-4274-b1e0-38bdd0d74147'")
    # print(cursor_factory.fetchall())
    #
    # nt_cursor  = connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    # nt_cursor.execute(
    #     "SELECT id, email, full_name, created_at, updated_at, verified, banned, roles FROM public.users WHERE id='d7864515-04d8-4274-b1e0-38bdd0d74147'")
    # print(nt_cursor.fetchall())


# 1. Поместить креды для подключения в `.env` файл
# 2. Создать модуль db_client, где попробовать реализовать функцию, которая подключается к БД мувиес, с выводом информации о PostgreSQL сервере
# 3. сделать новый модуль `db_creds` в папке `resources` и реализовать получение кредов из `.env` по аналогии с кредами юзерам
# - для подключения к бд импортировать в модуль эти креды