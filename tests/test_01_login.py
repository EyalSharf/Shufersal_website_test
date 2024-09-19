import allure
from pages.login_page import LoginPage



@allure.description("Log in with invalid credentials")
def test_login_with_invalid_credentials(driver):
    login_page = LoginPage(driver)
    login_page.login("invalid_username@example.com", "wrong password")
    assert login_page.verify_invalid_login()

@allure.description("Log in with valid credentials")
def test_login(driver):
    username = "eyal.sharf2@gmail.com"
    password = "Q1w2e3r4t5!"
    expected_greeting = "אייל"
    login_page = LoginPage(driver)

    login_page.login(username, password)

    assert login_page.verify_successful_login(
                                   expected_greeting), f"Login failed or unexpected greeting. Expected: {expected_greeting}"

