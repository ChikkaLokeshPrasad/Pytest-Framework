"""
tests/test_e2e_hybrid.py
"""

import time
import pytest
import allure

from pages.product_page import ProductPage
from api_client.notes_client import NotesAPIClient

from config.config import (
    UserEmail,
    UserPassword
)


@allure.feature("E2E UI API")
@pytest.mark.e2e
class TestUIToAPI:


    @allure.story("Create Note In UI Check In API")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ui_note_in_api(self, logged_in_driver):

        title = f"E2E {int(time.time())}"

        description = "Created in UI"

        home = ProductPage(logged_in_driver)

        home.create_note(
            title=title,
            description=description,
            category="Home"
        )

        assert home.is_note_in_ui(title)

        api = NotesAPIClient()

        api.login(
            UserEmail,
            UserPassword
        )

        response = api.get_notes()

        note = api.find_note_in_list(
            response,
            title
        )

        assert note is not None

        assert note["title"] == title

        assert note["description"] == description


    @allure.story("Check UI API Full Data")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ui_api_data_match(self, logged_in_driver):

        title = f"Match {int(time.time())}"

        description = "Checking full data"

        category = "Work"

        home = ProductPage(logged_in_driver)

        home.create_note(
            title=title,
            description=description,
            category=category
        )

        api = NotesAPIClient()

        api.login(
            UserEmail,
            UserPassword
        )

        response = api.get_notes()

        note = api.find_note_in_list(
            response,
            title
        )

        assert note is not None

        assert note["title"] == title

        assert note["description"] == description

        assert "id" in note


    @allure.story("Check Note Id")
    @allure.severity(allure.severity_level.NORMAL)
    def test_note_id_present(self, logged_in_driver):

        title = f"ID {int(time.time())}"

        home = ProductPage(logged_in_driver)

        home.create_note(
            category="Home",
            title=title,
            description="Id check"
        )

        api = NotesAPIClient()

        api.login(
            UserEmail,
            UserPassword
        )

        response = api.get_notes()

        note = api.find_note_in_list(
            response,
            title
        )

        assert note is not None

        assert "id" in note

        assert note["id"] != ""


@allure.feature("E2E UI API")
@pytest.mark.e2e
class TestAPIToUI:


    @allure.story("Delete Using API Check UI")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_api_delete_reflects_in_ui(self, logged_in_driver):

        title = f"Delete {int(time.time())}"

        home = ProductPage(logged_in_driver)

        home.create_note(
            category="Home",
            title=title,
            description="Delete test"
        )

        assert home.is_note_in_ui(title)

        api = NotesAPIClient()

        api.login(
            UserEmail,
            UserPassword
        )

        response = api.get_notes()

        note = api.find_note_in_list(
            response,
            title
        )

        assert note is not None

        note_id = note["id"]

        delete_response = api.delete_note(
            note_id
        )

        assert delete_response.status_code in [200, 204]

        home.driver.refresh()

        home.wait_for_dom_ready()

        assert not home.is_note_in_ui(title)


    @allure.story("Check Count After Delete")
    @allure.severity(allure.severity_level.NORMAL)
    def test_note_count_after_delete(self, logged_in_driver):

        title = f"Count {int(time.time())}"

        home = ProductPage(logged_in_driver)

        home.create_note(
            category="Home",
            title=title,
            description="Count test"
        )

        count_before = home.get_note_count()

        api = NotesAPIClient()

        api.login(
            UserEmail,
            UserPassword
        )

        response = api.get_notes()

        note = api.find_note_in_list(
            response,
            title
        )

        assert note is not None

        api.delete_note(note["id"])

        home.driver.refresh()

        home.wait_for_dom_ready()

        count_after = home.get_note_count()

        assert count_after < count_before


    @allure.story("Deleted Note Not In API")
    @allure.severity(allure.severity_level.NORMAL)
    def test_deleted_note_not_in_api(self, logged_in_driver):

        title = f"Remove {int(time.time())}"

        home = ProductPage(logged_in_driver)

        home.create_note(
            category="Home",
            title=title,
            description="Remove test"
        )

        api = NotesAPIClient()

        api.login(
            UserEmail,
            UserPassword
        )

        response = api.get_notes()

        note = api.find_note_in_list(
            response,
            title
        )

        assert note is not None

        api.delete_note(note["id"])

        new_response = api.get_notes()

        deleted_note = api.find_note_in_list(
            new_response,
            title
        )

        assert deleted_note is None