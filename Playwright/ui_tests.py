from fileinput import filename
from time import sleep
import pytest
from playwright.sync_api import sync_playwright,Page,expect
import time
from pathlib import Path
from datetime import datetime
# Создаем экземпляр Playwright и запускаем его
# playwright = sync_playwright().start()
#
# # Далее, используя объект playwright, можно запускать браузер и работать с ним
# browser = playwright.chromium.launch(headless=False)
# page = browser.new_page()
# page.goto('https://dev-cinescope.coconutqa.ru/')
# time.sleep(10)  # Сделаем sleep иначе браузер сразу закроектся перейдя к следующим строкам
#
# # После выполнения необходимых действий, следует явно закрыть браузер
# browser.close()
#
# # И остановить Playwright, чтобы освободить ресурсы
# playwright.stop()

from playwright.sync_api import sync_playwright
import time


# def test_multiple_browsers():
#     with sync_playwright() as p:
#      browser = p.chromium.launch(headless=False)
#      context1 = browser.new_context()
#      context2 = browser.new_context()
#
#      page1 = context1.new_page()
#      page2 = context1.new_page()
#      page3 = context2.new_page()
#      page4 = context2.new_page()
#
#      page1.goto("https://www.ya.ru")
#      page2.goto("https://www.vk.com")
#      page3.goto("https://www.ok.ru")
#      page4.goto("https://www.mail.ru")
#
#      time.sleep(10)
#
#      page1.close()
#      page2.close()
#      page3.close()
#      page4.close()
#
#      context2.close()
#      context1.close()
#
#      browser.close()
# DEFAULT_UI_TIMEOUT = 30000
#
# @pytest.fixture(scope="session")
# def browser(playwright):
#     browser = playwright.chromium.launhc(headless = False)
#     yield browser
#     browser.close()
#
# @pytest.fixture(scope="function")
# def context(browser):
#     context = browser.new_context()
#     context.tracing.start(screenshots=True,snapshots=True,sources=True)
#     context.set.default_timeout(DEFAULT_UI_TIMEOUT)
#     yield context
#     context.close()
# @pytest.fixture(scope="function")
# def page(context):
#     page = context.new_page()
#     yield page
#     page.close()
class Tools:
    @staticmethod
    def project_dir():
        return Path(__file__).parent.parent

    @staticmethod
    def files_dir(nested_directory: str = None, filename: str = None):
        """
        Возвращает путь к директории `files` (или её поддиректории).
        Если директория не существует, она создается.
        Если указан `filename`, возвращает полный путь к файлу.
        """
        files_path = Tools.project_dir() / "files"
        if nested_directory:
            files_path = files_path / nested_directory
        files_path.mkdir(parents=True, exist_ok=True)

        if filename:
            return files_path / filename
        return files_path

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
def test_text_box(page: Page):
    page.goto('https://demoqa.com/text-box')
    username_locator ="#userName"
    email_locator = "#userEmail"
    adress_locator = "#currentAddress"
    p_adress_locator = "#permanentAddress"
    button_locator = "#submit"
    page.fill(username_locator,"Алексей тут был")
    page.locator("#userName").fill("Алексей тут был не раз ")
    page.fill(email_locator,"Тут тже был")
    page.fill(selector="#userEmail", value="test@mail.ru")
    page.fill(adress_locator,"И сюда глянул")
    page.fill(p_adress_locator, "До сюда не дошел ")
    page.click(button_locator)
    expect(page.locator('#output #name')).to_have_text('Name:Алексей тут был не раз')
    expect(page.locator('#output #email')).to_have_text('Email:test@mail.ru')
    expect(page.locator('#output #currentAddress')).to_have_text('Current Address :И сюда глянул')
    expect(page.locator('#output #permanentAddress')).to_have_text('Permananet Address :До сюда не дошел')


time.sleep(10)

def test_form(page):
    page.goto("https://demoqa.com/text-box")
    page.get_by_role("textbox", name="Full Name").fill("Тут был Алексей")
    page.get_by_role("textbox", name="name@example.com").fill("tuttozh@ebil.com")
    page.get_by_role("textbox", name="Current Address").fill("HMSAP")
    page.locator("#permanentAddress").fill("QWERTY")
    page.get_by_role("button", name="Submit").click()

    expect(page.locator('#output #name')).to_have_text('Name:Тут был Алексей')
    expect(page.locator('#output #email')).to_have_text('Email:tuttozh@ebil.com')
    expect(page.locator('#output #currentAddress')).to_have_text('Current Address :HMSAP')
    expect(page.locator('#output #permanentAddress')).to_have_text('Permananet Address :QWERTY')

def test_selectors(page):
    page.goto("https://demoqa.com/webtables")
    page.get_by_role("button", name = "Add").click()
    #page.locator(utton:has-text("Add")')'b.click()
    expect(page.get_by_text('Registration Form')).to_be_visible()
    page.get_by_placeholder("First Name").fill("Alexey")
    page.locator("#lastName").fill("чАЧАЧА")
    page.get_by_placeholder("name@example.com").fill("name@example.com")
    page.get_by_placeholder("Age").fill("47")
    page.get_by_placeholder("Salary").fill("1000000")
    page.get_by_placeholder("Department").fill("QA")
    page.pause()
    page.get_by_role("button",name="Submit").click()

def test_new_tselectors(page):
    page.goto("https://demoqa.com/automation-practice-form")
    page.locator("#firstName").type("Алексей")
    page.get_by_role("textbox",name="Last Name").fill("чёкаво")
    page.get_by_role("textbox",name="name@example.com").type("ball@mail.ru")
    page.check('#gender-radio-1')
    page.get_by_role("textbox",name="Mobile Number").fill("89076381933")
    date_user = page.locator("#dateOfBirthInput").get_attribute("value")
    today = datetime.now()
    date_form = today.strftime("%d %b %Y")
    assert date_user == date_form
    text_ui = "© 2013-2026 TOOLSQA.COM | ALL RIGHTS RESERVED."
    text = page.locator("footer span").inner_text()
    assert text_ui == text

def test_enabled_radio(page):
    page.goto("https://demoqa.com/radio-button")
    page.is_enabled("#yesRadio")
    page.get_by_role("radio",name="Impressive").is_enabled()
    page.is_disabled("#noRadio")

def test_visible_home(page):
    page.goto("https://demoqa.com/checkbox")
    page.is_visible("#Select Home")
    page.is_hidden("#Select Desktop")
    page.click(".rc-tree-switcher")
    page.screenshot(path="screen.png")
    page.pause()
    page.is_visible("#Select Desktop")

def test_visible_dynamic(page):
    page.goto("https://demoqa.com/dynamic-properties")
    page.is_hidden("#visibleAfter")
    page.wait_for_selector("#visibleAfter",state="visible",timeout=6000)

def test_expect(page: Page):
    page.goto("https://demoqa.com/radio-button")
    yes_radio = page.get_by_role("radio", name="Yes")
    impressive_radio = page.get_by_role("radio", name="Impressive")
    no_radio = page.get_by_role("radio", name="No")
    expect(no_radio).to_be_disabled()  # проверяем, что не доступен
    expect(yes_radio).to_be_enabled()  # проверяем, что доступен
    expect(impressive_radio).to_be_enabled()  # проверяем, что доступен
    page.locator('[for="yesRadio"]').click()  # тут хитрый лейбл не позволяет кликнуть прямо на инпут, обращаемся по лейблу
    expect(yes_radio).to_be_checked()  # проверяем, что отмечен
    expect(impressive_radio).not_to_be_checked()  # проверяем, что не отмечен
