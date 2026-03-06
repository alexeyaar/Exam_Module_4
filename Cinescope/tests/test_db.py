from utils.data_generator import DataGenerator
import pytest
from db_models.user import AccountTransactionTemplate
import allure


@allure.epic("Тестирование транзакций")
@allure.feature("Тестирование транзакций между счетами")
class TestDB:
    def test_get_user_by_id(self, super_admin, db_helper, created_test_user):
        assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
        assert db_helper.user_exists_by_email("api1@gmail.com")

    def test_get_user_by_email(self,created_test_user,db_helper):
        print(created_test_user.email,created_test_user.full_name)
        assert created_test_user ==db_helper.get_user_by_email(created_test_user.email)

    def test_create_movie(self,db_helper,data_movie_db):
       name = data_movie_db["name"]
       assert db_helper.get_movies_by_name(name) is None,f"Фильм существует в базе"
       create_movie = db_helper.create_movie(data_movie_db)
       assert create_movie is not None
       get_movie =  db_helper.get_movies_by_name(name)
       assert get_movie.name == name

    @allure.story("Корректность перевода денег между двумя счетами")
    @allure.description("""
       Этот тест проверяет корректность перевода денег между двумя счетами.
       Шаги:
       1. Создание двух счетов: Stan и Bob.
       2. Перевод 200 единиц от Stan к Bob.
       3. Проверка изменения балансов.
       4. Очистка тестовых данных.
       """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Alexey Artemov")
    @allure.title("Тест перевода денег между счетами 200 рублей")

    def test_accounts_transaction_template(self,db_session):
        with allure.step("Создание тестовых данных в базе данных: счета Stan и Bob"):
            stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_name()}", balance=1000)
            bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_name()}", balance=500)

        db_session.add_all([stan, bob])
        db_session.commit()

        @allure.step("Функция перевода денег: transfer_money")
        @allure.description("""
                   функция выполняющая транзакцию, имитация вызова функции на стороне тестируемого сервиса
                   и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
                   """)
        def transfer_money(session, from_account, to_account, amount):
            with allure.step(" Получаем счета"):
                from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
                to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

            with allure.step("Проверяем, что на счете достаточно средств"):
             if from_account.balance < amount:
                raise ValueError("Недостаточно средств на счете")

            with allure.step("Выполняем перевод"):
                from_account.balance -= amount
                to_account.balance += amount

            with allure.step("Сохраняем изменения"):
                session.commit()

        # ====================================================================== Тест
        with allure.step("Проверяем начальные балансы"):
            assert stan.balance == 1000
            assert bob.balance == 500

        try:
            with allure.step("Выполняем перевод 200 единиц от stan к bob"):
                transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)

            with allure.step("Проверяем, что балансы изменились"):
                assert stan.balance == 800
                assert bob.balance == 700

        except Exception as e:
            with allure.step("ОШИБКА откаты транзакции"):
                db_session.rollback()  # откат всех введеных нами изменений
            pytest.fail(f"Ошибка при переводе денег: {e}")

        finally:
            with allure.step("Удаляем данные для тестирования из базы"):
                db_session.delete(bob)
                # Фиксируем изменения в базе данных
                db_session.commit()