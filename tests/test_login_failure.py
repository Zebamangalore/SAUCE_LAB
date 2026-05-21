"""test_login_failure.py – verifies error handling for bad credentials."""

import pytest
from pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.login
class TestLoginFailure:
    """Groups all negative-login scenarios."""

    def test_invalid_username_and_password(
        self, login_page: LoginPage, invalid_creds: dict
    ):
        """
        GIVEN  randomly generated (invalid) credentials
        WHEN   the user submits the login form
        THEN   an error message is displayed
        AND    the user remains on the login page
        """
        login_page.open().login(
            username=invalid_creds["username"],
            password=invalid_creds["password"],
        )

        assert login_page.is_error_visible(), "Error message should be visible"
        error_text = login_page.get_error_message()
        assert "Username and password do not match" in error_text, (
            f"Unexpected error message: '{error_text}'"
        )
        assert "inventory" not in login_page.get_current_url(), (
            "User should NOT be redirected to inventory on failed login"
        )

    def test_empty_username(self, login_page: LoginPage, valid_creds: dict):
        """
        GIVEN  a blank username with a valid password
        WHEN   the form is submitted
        THEN   an error prompts for a username
        """
        login_page.open().login(username="", password=valid_creds["password"])

        assert login_page.is_error_visible(), "Error message should be visible"
        assert "Username is required" in login_page.get_error_message()

    def test_empty_password(self, login_page: LoginPage, valid_creds: dict):
        """
        GIVEN  a valid username with a blank password
        WHEN   the form is submitted
        THEN   an error prompts for a password
        """
        login_page.open().login(username=valid_creds["username"], password="")

        assert login_page.is_error_visible(), "Error message should be visible"
        assert "Password is required" in login_page.get_error_message()

    def test_locked_out_user(self, login_page: LoginPage):
        """
        GIVEN  the known locked-out account
        WHEN   the user logs in
        THEN   a 'locked out' error is shown
        """
        login_page.open().login(
            username="locked_out_user", password="secret_sauce"
        )

        assert login_page.is_error_visible(), "Error message should be visible"
        assert "locked out" in login_page.get_error_message().lower(), (
            f"Expected 'locked out' message, got: '{login_page.get_error_message()}'"
        )