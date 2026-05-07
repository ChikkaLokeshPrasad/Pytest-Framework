"""
tests/test_api_notes.py
"""

import time
import pytest
import allure

from api_client.notes_client import NotesAPIClient


@allure.feature("API - Notes")
@pytest.mark.api
class TestAPIGetNotes:


    @allure.story("Get Notes - Status Code")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_notes_status_200(self, api_client):

        response = api_client.get_notes()

        assert response.status_code == 200, \
            f"Expected 200 but got {response.status_code}"


    @allure.story("Get Notes - Response Structure")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_notes_response_structure(self, api_client):

        response = api_client.get_notes()

        body = response.json()

        assert "data" in body, \
            "'data' key missing in response"

        assert isinstance(body["data"], list), \
            "'data' is not a list"


    @allure.story("Get Notes - Response Time")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_notes_response_time(self, api_client):

        start = time.time()

        response = api_client.get_notes()

        end = time.time()

        total_time = end - start

        allure.attach(
            str(total_time),
            name="response_time",
            attachment_type=allure.attachment_type.TEXT
        )

        assert response.status_code == 200

        assert total_time < 2, \
            f"API too slow. Time taken: {total_time}"


@allure.feature("API - Notes")
@pytest.mark.api
class TestAPICreateNote:


    @allure.story("Create Note")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_note_returns_201(self, api_client):

        title = f"API Note {int(time.time())}"

        response = api_client.create_note(
            title=title,
            description="Created using API test",
            category="Home"
        )

        assert response.status_code in [200, 201], \
            f"Expected 200 or 201 but got {response.status_code}"


    @allure.story("Create Note - Verify Data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_note_data_matches(self, api_client):

        title = f"Title Match {int(time.time())}"

        description = "Checking response data"

        response = api_client.create_note(
            title=title,
            description=description,
            category="Work"
        )

        body = response.json()

        data = body.get("data", {})

        assert data.get("title") == title, \
            "Title mismatch"

        assert data.get("description") == description, \
            "Description mismatch"

        assert "id" in data, \
            "Id missing in response"


    @allure.story("Create Note - Verify In Notes List")
    @allure.severity(allure.severity_level.NORMAL)
    def test_created_note_visible_in_get_notes(self, api_client):

        title = f"List Check {int(time.time())}"

        api_client.create_note(
            title=title,
            description="Check note in list",
            category="Personal"
        )

        response = api_client.get_notes()

        note = api_client.find_note_in_list(
            response,
            title
        )

        assert note is not None, \
            f"Note '{title}' not found in notes list"


    @allure.story("Create Note - Empty Title")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_note_empty_title(self, api_client):

        response = api_client.create_note(
            title="",
            description="No title",
            category="Home"
        )

        assert response.status_code in [400, 422], \
            f"Expected 400 or 422 but got {response.status_code}"


    @allure.story("Create Note Without Login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_note_without_auth(self):

        client = NotesAPIClient()

        response = client.create_note(
            title="Unauthorized",
            description="Should fail"
        )

        assert response.status_code == 401, \
            f"Expected 401 but got {response.status_code}"


@allure.feature("API - Notes")
@pytest.mark.api
class TestAPIDeleteNote:


    @allure.story("Delete Note")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_note_success(self, api_client):

        title = f"Delete Note {int(time.time())}"

        create_response = api_client.create_note(
            title=title,
            description="Will be deleted"
        )

        body = create_response.json()

        note_id = body["data"]["id"]

        delete_response = api_client.delete_note(note_id)

        assert delete_response.status_code in [200, 204], \
            f"Expected 200 or 204 but got {delete_response.status_code}"


    @allure.story("Deleted Note Not In List")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_deleted_note_not_present(self, api_client):

        title = f"Delete Check {int(time.time())}"

        create_response = api_client.create_note(
            title=title,
            description="Delete verification"
        )

        note_id = create_response.json()["data"]["id"]

        api_client.delete_note(note_id)

        response = api_client.get_notes()

        note = api_client.find_note_in_list(
            response,
            title
        )

        assert note is None, \
            f"Deleted note '{title}' still present"


    @allure.story("Delete Invalid Note")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_delete_invalid_note(self, api_client):

        response = api_client.delete_note(
            "000000000000000000000000"
        )

        assert response.status_code in [400, 404], \
            f"Expected 400 or 404 but got {response.status_code}"