import time
from utils.data_generator import DataGenerator
from playwright.sync_api import Page, expect,sync_playwright
from random import randint
import time
import allure
import pytest
from models.page_odjects_models import CinescopeRegisterPage, CinescopLoginPage


# def test_register(page):
#     locator_name = '[placeholder="Имя Фамилия Отчество"]'
#     email_locator = '[name="email"]'
#     password_locator = '[name="password"]'
#     pass_repeat_locator = '[name="passwordRepeat"]'
#     password=DataGenerator.generate_random_password()
#     button_locator = '[type="submit"]'
#     page.goto("https://dev-cinescope.coconutqa.ru/register")
#     page.fill(locator_name,"Алексей А.А")
#     page.fill(email_locator,DataGenerator.generate_random_email())
#     page.fill(password_locator,password)
#     page.fill(pass_repeat_locator,password)
#     page.click(button_locator)
#
#     page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
#     expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)
#
@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestloginPage:
    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self, registered_user):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=False)  # Запуск браузера headless=False для визуального отображения
            page = browser.new_page()
            login_page = CinescopLoginPage(page)  # Создаем объект страницы Login

            login_page.open()
            login_page.login(registered_user.email, registered_user.password)  # Осуществяем вход
            login_page.check_error_allert()
            login_page.make_screenshot_and_attach_to_allure()  # Прикрепляем скриншот
            #login_page.assert_allert_was_pop_up()  # Проверка появления и исчезновения алерта

            # Пауза для визуальной проверки (нужно удалить в реальном тестировании)
            browser.close()


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
    @allure.title("Проведение успешной регистрации")
    def test_register_by_ui(self):
        with sync_playwright() as playwright:
            # Подготовка данных для регистрации
            random_email = DataGenerator.generate_random_email()
            random_name = DataGenerator.generate_random_name()
            random_password = DataGenerator.generate_random_password()

            browser = playwright.chromium.launch(
                headless=False)  # Запуск браузера headless=False для визуального отображения
            page = browser.new_page()

            register_page = CinescopeRegisterPage(page)  # Создаем объект страницы регистрации cinescope
            register_page.open()
            register_page.register(f"PlaywrightTest {random_name}", random_email, random_password,
                                   random_password)  # Выполняем регистрацию

            register_page.assert_was_redirect_to_login_page()  # Проверка редиректа на страницу /login
            register_page.make_screenshot_and_attach_to_allure()  # Прикрепляем скриншот
            register_page.assert_allert_was_pop_up()  # Проверка появления и исчезновения алерта

            # Пауза для визуальной проверки (нужно удалить в реальном тестировании)
            browser.close()

