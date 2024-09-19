import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    enter = (By.LINK_TEXT, "כניסה")
    user_name = (By.ID, "j_username")
    password = (By.ID, "j_password")
    button = (By.CSS_SELECTOR, "button.btn-login.btn-big")

    def login(self, username, password):
        self.driver.get("https://www.shufersal.co.il/online/")
        self.driver.find_element(*self.enter).click()
        self.driver.find_element(*self.user_name).send_keys(username)
        self.driver.find_element(*self.password).send_keys(password)
        self.driver.find_element(*self.button).click()

    def verify_invalid_login(self):
        try:
            wait = WebDriverWait(self.driver, 30)
            error_message_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-body p[role='alert']"))
            )
            error_message = error_message_element.text.strip()

            success_message = f"Invalid login detected. Error message: '{error_message}'"
            print(success_message)
            allure.attach(success_message, name="Invalid Login Detected", attachment_type=allure.attachment_type.TEXT)

            return error_message
        except TimeoutException as e:
            error_message = f"Failed to find error message for invalid login: {str(e)}"
            print(error_message)
            allure.attach(error_message, name="Invalid Login Error", attachment_type=allure.attachment_type.TEXT)
            raise TimeoutException(error_message)

    import allure

    def verify_successful_login(self, expected_greeting):
        try:
            wait = WebDriverWait(self.driver, 45)
            user_greeting = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span[role='heading'][aria-level='3']"))
            )
            actual_greeting = user_greeting.text.strip()
            if actual_greeting == expected_greeting:
                success_message = f"Login successful. Greeting matched: '{actual_greeting}'"
                print(success_message)
                allure.attach(success_message, name="Login Success", attachment_type=allure.attachment_type.TEXT)
                return True
            else:
                failure_message = f"Login failed. Expected greeting: '{expected_greeting}', Actual greeting: '{actual_greeting}'"
                print(failure_message)
                allure.attach(failure_message, name="Login Failure", attachment_type=allure.attachment_type.TEXT)
                return False
        except TimeoutException as e:
            error_message = f"Failed to find user greeting element: {str(e)}"
            print(error_message)
            allure.attach(error_message, name="Login Error", attachment_type=allure.attachment_type.TEXT)
            raise TimeoutException(error_message)
