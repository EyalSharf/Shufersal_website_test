import allure
import pytest
from selenium import webdriver
import sys
import os

# Get the absolute path of the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project root to the Python path
sys.path.insert(0, project_root)

print(f"Updated sys.path: {sys.path}")  # This will help us debug


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(autouse=True)
def take_screenshot_after_test(request, driver):
    yield
    screenshot_name = f"screenshot_{request.node.name}.png"
    driver.save_screenshot(screenshot_name)
    with allure.step("Taking screenshot after test"):
        allure.attach.file(screenshot_name, name="Test Screenshot", attachment_type=allure.attachment_type.PNG)
