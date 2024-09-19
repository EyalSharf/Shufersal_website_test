import time
from selenium.common import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Checkout:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def click_element(self, by, value, max_attempts=3):
        for attempt in range(max_attempts):
            try:
                wait = WebDriverWait(self.driver, 40)
                button = wait.until(EC.element_to_be_clickable((by, value)))
                button.click()
                return True
            except (StaleElementReferenceException, ElementClickInterceptedException):
                time.sleep(1)
        return False

    def click_confirm_button(self, max_attempts=5, wait_time=10):
        locators = [
            (By.CSS_SELECTOR, 'button.btn.big.btn-primary.btn-block[type="submit"]'),
            (By.XPATH, '//button[contains(@class, "btn-primary") and contains(text(), "אישור")]'),
            (By.XPATH, '//button[text()="אישור"]')
        ]
        for attempt in range(max_attempts):
            for locator in locators:
                try:
                    wait = WebDriverWait(self.driver, wait_time)
                    button = wait.until(EC.element_to_be_clickable(locator))
                    button.click()
                    return True
                except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException):
                    continue
            time.sleep(2)
        return False

    def wait_for_confirmation_button(self):
        max_attempts = 5
        wait_time = 2
        for attempt in range(max_attempts):
            try:
                wait = WebDriverWait(self.driver, wait_time)
                confirmation = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//a[@class='btnConfirm' and contains(., 'אישור תשלום')]"))
                )
                if confirmation.is_displayed():
                    print("Order confirmation button found.")
                    return True
            except (TimeoutException, AssertionError):
                try:
                    wait = WebDriverWait(self.driver, wait_time)
                    delivery_payment_header = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//h1[@class='title' and contains(text(), 'פרטי משלוח ותשלום')]"))
                    )
                    if delivery_payment_header.is_displayed():
                        print("Delivery and payment details header found.")
                        return True
                except (TimeoutException, AssertionError):
                    print(
                        f"Failed to find confirmation button or delivery details header on attempt {attempt + 1}. Retrying...")

        raise Exception("Neither order confirmation button nor delivery details header found after multiple attempts")
