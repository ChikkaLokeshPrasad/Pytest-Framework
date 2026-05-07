import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from api_client.notes_client import NotesAPIClient
import os
import allure

# --------------------------------
# Selenium Driver Fixture
# --------------------------------
@pytest.fixture
def driver():

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)

    driver.maximize_window()

    yield driver

    driver.quit()


# --------------------------------
# Logged In Driver Fixture
# --------------------------------
@pytest.fixture
def logged_in_driver(driver):

    from pages.login_page import LoginPage
    from config.config import (
        UserEmail,
        UserPassword
    )

    page = LoginPage(driver).open()

    page.login(UserEmail, UserPassword)

    page.wait_for_url_contains("notes/app")

    return driver


# --------------------------------
# API Client Fixture
# --------------------------------
@pytest.fixture
def api_client():

    from config.config import (
        UserEmail,
        UserPassword
    )

    client = NotesAPIClient()

    # login and store token
    client.login(
        email=UserEmail,
        password=UserPassword
    )

    return client





@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item,
    call,
):

    outcome = yield

    report = outcome.get_result()

    # Only capture on test failure
    if (
        report.when == "call"
        and report.failed
    ):

        driver = item.funcargs.get("driver")

        if driver:

            screenshots_dir = (
                "reports/screenshots"
            )

            os.makedirs(
                screenshots_dir,
                exist_ok=True
            )

            screenshot_path = (
                f"{screenshots_dir}/"
                f"{item.name}.png"
            )

            # Save screenshot
            driver.save_screenshot(
                screenshot_path
            )

            # Attach to Allure
            allure.attach.file(
                screenshot_path,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )