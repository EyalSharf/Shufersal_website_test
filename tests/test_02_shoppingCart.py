import allure
from pages.login_page import LoginPage
from pages.shopping_cart import Shopping_Cart


@allure.description("add bread to the shopping cart")
def test_add_first_product(driver):
    username = "eyal.sharf2@gmail.com"
    password = "Q1w2e3r4t5!"
    login_page = LoginPage(driver)
    shopping_cart = Shopping_Cart(driver)
    login_page.login(username, password)
    shopping_cart.click_cart_toggle_button()
    shopping_cart.clear_cart_if_present()
    search_term = "לחם אחיד פרוס"
    shopping_cart.perform_search(search_term), "Failed to search for bread"
    shopping_cart.add_product_to_cart()

    assert shopping_cart.verify_item_added_to_cart(search_term), "Item was not added to the cart or not found."


@allure.description("add milk to the shopping cart")
def test_add_second_product(driver):
    search_term = "חלב"
    shopping_cart = Shopping_Cart(driver)
    shopping_cart.perform_search(search_term), "Failed to search for milk"
    shopping_cart.add_product_to_cart()

    assert shopping_cart.verify_item_added_to_cart(search_term), "Item was not added to the cart or not found."


@allure.description("add cheese to the shopping cart")
def test_add_third_product(driver):
    search_term = "פרוסות גבינה צהובה"
    shopping_cart = Shopping_Cart(driver)
    shopping_cart.perform_search(search_term), "Failed to search for cheese"
    shopping_cart.add_product_to_cart()

    assert shopping_cart.verify_item_added_to_cart(search_term), "Item was not added to the cart or not found."


@allure.description("add pastrami to the shopping cart")
def test_add_fourth_product(driver):
    search_term = "פסטרמה"
    shopping_cart = Shopping_Cart(driver)
    shopping_cart.perform_search(search_term), "Failed to search for pastrami"
    shopping_cart.add_product_to_cart()

    assert shopping_cart.verify_item_added_to_cart(search_term), "Item was not added to the cart or not found."


@allure.description("input invalid characters")
def test_input_invalid_char(driver):
    search_term = "!@#$"
    expected_alert_text = "הוזן תו לא חוקי"
    shopping_cart = Shopping_Cart(driver)

    search_success, alert_text = shopping_cart.perform_search(search_term)

    if alert_text:
        assert alert_text == expected_alert_text, f"Unexpected alert message: {alert_text}"
    elif not search_success:
        # If search failed but no alert, check for an error message on the page
        error_message = shopping_cart.get_error_message()
        assert error_message == expected_alert_text, f"Unexpected error message: {error_message}"
    else:
        assert False, "Search succeeded unexpectedly with invalid input"

