import time
import allure
from selenium.common import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, \
    JavascriptException, NoAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Shopping_Cart:
    def __init__(self, driver):
        self.search_results = None
        self.error_message = None
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    SEARCH_INPUT = (By.ID, "js-site-search-input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.btnSubmit.js_search_button")
    SEARCH_RESULTS = (By.CSS_SELECTOR, "li.SEARCH.tileBlock")
    def perform_search(self, search_term, max_attempts=5):
        for attempt in range(max_attempts):
            try:
                self._clear_and_fill_search_input(search_term)
                self._click_search_button()

                alert_text = self._check_for_alert()
                if alert_text:
                    return False, alert_text

                self._wait_for_search_results()
                return True, None

            except (TimeoutException, ElementClickInterceptedException,
                    StaleElementReferenceException, JavascriptException) as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_attempts - 1:
                    print("Retrying...")
                    time.sleep(2)
        return False, None

    def _clear_and_fill_search_input(self, search_term):
        searchbar = self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))
        self.driver.execute_script("arguments[0].value = '';", searchbar)
        for char in search_term:
            searchbar.send_keys(char)
            time.sleep(0.1)

    def _click_search_button(self):
        search_button = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        search_button.click()

    def _check_for_alert(self, timeout=3):
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()
            print(f"Alert detected: {alert_text}")
            return alert_text
        except TimeoutException:
            return None

    def _wait_for_search_results(self):
        self.wait.until(EC.presence_of_element_located(self.SEARCH_RESULTS))

    PRODUCT_BLOCKS = (By.CSS_SELECTOR, "li.SEARCH.tileBlock")
    ADD_TO_CART_BUTTON = (By.XPATH, ".//button[contains(@class, 'js-add-to-cart') and contains(text(), 'הוספה')]")
    PRODUCT_NAME_IN_CART = (By.XPATH, "//h3[@class='miglog-text3 miglog-prod-name ']")
    CART_TOGGLE_BUTTON = (By.CSS_SELECTOR, "button.icon.icon-arrow-1.hidden-lg-max-header.btnToggle.bouncingArrow")
    CART_CONTENT = (By.CSS_SELECTOR, "#cartMiddleContent")
    CLEAR_CART_BUTTON = (
            By.CSS_SELECTOR, "div.col-xs-6.deleteCartContainer a[data-miglog-role='cart-remove-overlay-opener']")
    CONFIRM_CLEAR_CART_BUTTON = (By.CSS_SELECTOR, "button.btn-radius.outline[data-miglog-role='cart-remover']")
    CART_ITEMS = (By.CSS_SELECTOR, "div.cart-items")
    ERROR_MESSAGE = (By.ID, "error-message")

    def add_product_to_cart(self):
        product_blocks = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_BLOCKS))
        first_product = product_blocks[0]
        add_button = first_product.find_element(*self.ADD_TO_CART_BUTTON)
        self.driver.execute_script("arguments[0].click();", add_button)
        time.sleep(2)

    def verify_item_added_to_cart(self, search_term, wait_time=45):
        try:
            product_elements = self.wait.until(
                EC.presence_of_all_elements_located(self.PRODUCT_NAME_IN_CART)
            )

            search_terms = search_term.split()
            for product_element in product_elements:
                cart_text = product_element.text
                if any(term_part in cart_text for term_part in search_terms):
                    print(f"Product matching search term '{search_term}' found in cart: '{cart_text}'.")
                    return True

            print(f"Expected product containing any part of '{search_term}' not found in cart.")
            return False

        except TimeoutException:
            print(f"Failed to verify that '{search_term}' or part of it was added to the cart.")
            return False

    def click_cart_toggle_button(self, timeout=30):
        try:
            self.wait_for_page_load()
            self.wait_for_overlay_disappearance()

            button = self.wait.until(EC.element_to_be_clickable(self.CART_TOGGLE_BUTTON))
            self.scroll_into_view(button)
            time.sleep(1)

            self.click_element(button)
            self.wait.until(lambda d: d.find_element(*self.CART_CONTENT))

            self.log_success("Successfully clicked the cart toggle button")
            return True
        except Exception as e:
            self.log_error(f"Failed to click the cart toggle button: {str(e)}")
            raise

    def clear_cart_if_present(self, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            try:
                clear_cart_button = wait.until(EC.presence_of_element_located(self.CLEAR_CART_BUTTON))
                print("Clear cart button found")
            except TimeoutException:
                print(f"Clear cart button not found within {timeout} seconds. Continuing with the script.")
                return False

            self.click_element(clear_cart_button)

            try:
                confirm_button = wait.until(EC.element_to_be_clickable(self.CONFIRM_CLEAR_CART_BUTTON))
                confirm_button.click()
                print("Confirmation dialog 'כן, רוקנו את הסל' clicked")

                wait.until(EC.invisibility_of_element_located(self.CART_ITEMS))
                print("Cart cleared successfully")
            except TimeoutException:
                print("No confirmation dialog appeared or it couldn't be interacted with")
            except Exception as e:
                print(f"Error while handling confirmation dialog: {str(e)}")

            return True

        except Exception as e:
            print(f"Unexpected error in clear_cart_if_present: {str(e)}")
            return False

    def check_and_dismiss_alert(self, timeout=5):
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert_text = alert.text
            alert.dismiss()
            return alert_text
        except TimeoutException:
            return None

    def get_error_message(self, timeout=5):
        try:
            error_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text
        except TimeoutException:
            return None

    # Helper methods
    def wait_for_page_load(self):
        self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

    def wait_for_overlay_disappearance(self):
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.overlay")))

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def click_element(self, element):
        try:
            element.click()
        except:
            ActionChains(self.driver).move_to_element(element).click().perform()

    def log_success(self, message):
        print(message)
        allure.attach(message, name="Success", attachment_type=allure.attachment_type.TEXT)

    def log_error(self, message):
        print(message)
        allure.attach(message, name="Error", attachment_type=allure.attachment_type.TEXT)