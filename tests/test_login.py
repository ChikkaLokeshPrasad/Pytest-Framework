import pytest
import allure
from pages.login_page import LoginPage
from config.config import UserEmail, UserPassword
from pages.product_page import ProductPage



@allure.feature("UI — Login")
@pytest.mark.ui
class TestLogin:

    @allure.story("TC-UI-01: Valid credentials — successful login")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, driver):
        """FR-01: User logs in with valid credentials and lands on Notes dashboard."""
        with allure.step("Open login page"):
            page = LoginPage(driver).open()

        with allure.step("Submit valid credentials"):
            page.login(UserEmail, UserPassword)

        with allure.step("Assert redirect to Notes App"):
            home = ProductPage(driver)
            assert home.wait_for_url_contains("notes/app"), \
                "Expected redirect to /notes/app after login"

        with allure.step("Assert Notes dashboard is visible"):
            assert home.is_element_present(home.ADD_NOTE_BTN), \
                "Add Note button not visible — login may have failed"

    @allure.story("TC-NEG-01: Invalid credentials — error message shown")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_credentials_shows_error(self, driver):
        """FR-09: Invalid email/password should show an error; user stays on login."""
        page = LoginPage(driver).open()
        page.login("invalid@nowhere.com", "WrongPass999!")

        with allure.step("Assert error message is displayed"):
            assert page.is_error_displayed(), \
                "Expected an error message for invalid credentials"
            msg = page.get_error_message()
            assert msg, f"Error message text should not be empty, got: '{msg}'"
            allure.attach(msg, name="error_message",
                          attachment_type=allure.attachment_type.TEXT)

    @allure.story("TC-NEG-02: Empty fields — login blocked")
    @allure.severity(allure.severity_level.MINOR)
    def test_empty_fields_blocked(self, driver):
        """FR-09: Submitting empty form should not navigate away from login page."""
        page = LoginPage(driver).open()
        page.click_login()

        with allure.step("Assert user remains on login page"):
            assert page.is_on_login_page(), \
                "User should not leave login page when fields are empty"

    @allure.story("TC-NEG-03: Wrong password only — error shown")
    @allure.severity(allure.severity_level.NORMAL)
    def test_wrong_password_shows_error(self, driver):
        """FR-09: Correct email with wrong password should show error."""
        page = LoginPage(driver).open()
        page.login(UserEmail, "CompletelyWrongPassword!")

        assert page.is_error_displayed(), \
            "Expected error for correct email with wrong password"
