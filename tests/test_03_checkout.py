from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.checkout import Checkout
from pages.login_page import LoginPage
import allure
from selenium.webdriver.common.by import By


@allure.description("Login with invalid credentials")
def test_shufersal_invalid_login(driver):
    username = "eyal.sharf2@gmail.com"
    password = "Q1w2e3r4t5!"
    login_page = LoginPage(driver)
    checkout = Checkout(driver)
    login_page.login(username, password)
    checkout.click_element(By.CSS_SELECTOR,
                           'a.btnSubmit[data-miglog-role="cart-summary-link"]'), "Failed to click checkout button"
    checkout.click_element(By.CSS_SELECTOR,
                           'button[data-url="/online/he/checkout"]'), "Failed to continue to checkout"

    wait = WebDriverWait(driver, 20)
    input_pass = wait.until(EC.element_to_be_clickable((By.ID, "j_password")))
    input_pass.send_keys('12345678!')

    checkout.click_confirm_button(), "Failed to click confirm button"
    # Wait for the error message to appear
    wait = WebDriverWait(driver, 10)
    error_message = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "span.field-validation-error[data-valmsg-for='j_password'] span.error.colorError")))

    # Assert that the error message is displayed and contains the correct text
    assert error_message.is_displayed(), "Error message not displayed for invalid credentials"
    assert error_message.text.strip() == "סיסמה לא תקינה", "Unexpected error message text"


@allure.description("check out")
def test_shufersal_checkout(driver):
    action = ActionChains(driver)
    action.send_keys(Keys.ESCAPE).perform()
    checkout = Checkout(driver)
    checkout.click_element(By.CSS_SELECTOR,
                           'button[data-url="/online/he/checkout"]'), "Failed to continue to checkout"

    wait = WebDriverWait(driver, 20)
    input_pass = wait.until(EC.element_to_be_clickable((By.ID, "j_password")))
    input_pass.send_keys('Q1w2e3r4t5!')

    checkout.click_confirm_button(), "Failed to click confirm button"

    assert checkout.wait_for_confirmation_button()
