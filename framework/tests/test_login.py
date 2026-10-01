"""Login module - 10 tests. Each test gets a fresh browser (fixture 'driver')."""
import time

import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils import config_reader as cfg
from utils.excel_reader import read_rows

USER = cfg.get("app", "username")
PWD = cfg.get("app", "password")

pytestmark = pytest.mark.login        # every test in this file belongs to group "login"


@pytest.mark.smoke
@pytest.mark.order(1)                 # priority = 1
def test_valid_login(driver):
    page = LoginPage(driver).load()
    page.login(USER, PWD)
    assert page.is_logged_in(), "Valid user should reach the Home page"


@pytest.mark.regression
def test_login_page_title_and_fields(driver):
    page = LoginPage(driver).load()
    assert driver.title == "Login"
    assert page.find("username").get_attribute("placeholder") == "Email or Mobile No"
    assert page.find("password").get_attribute("type") == "password"


@pytest.mark.regression
def test_invalid_password(driver):
    page = LoginPage(driver).load()
    page.login(USER, "wrongpassword")
    time.sleep(3)
    assert page.is_on_login_page(), "Wrong password must not log in"


@pytest.mark.regression
def test_invalid_username(driver):
    page = LoginPage(driver).load()
    page.login("nobody_" + str(int(time.time())) + "@test.com", PWD)
    time.sleep(3)
    assert page.is_on_login_page()


@pytest.mark.regression
def test_empty_username_and_password(driver):
    page = LoginPage(driver).load()
    driver.execute_script("document.getElementById('UserName').value='';"
                          "document.getElementById('Password').value='';")
    page.click("sign_in")
    shown = page.is_visible("username_error") or page.page_has_text("Please fill all the required field", 5)
    assert shown, "A 'required field' message should be shown"
    assert page.is_on_login_page()


@pytest.mark.regression
def test_empty_password_only(driver):
    page = LoginPage(driver).load()
    page.type("username", USER)
    driver.execute_script("document.getElementById('Password').value='';")
    page.click("sign_in")
    shown = page.is_visible("password_error") or page.page_has_text("Please fill all the required field", 5)
    assert shown, "A 'required field' message should be shown"
    assert page.is_on_login_page()


@pytest.mark.regression
def test_remember_me_checkbox(driver):
    page = LoginPage(driver).load()
    assert not page.find("remember_me").is_selected()
    page.click("remember_label")
    if not page.find("remember_me").is_selected():
        driver.execute_script("arguments[0].click();", page.find("remember_me"))
    assert page.find("remember_me").is_selected()


@pytest.mark.regression
def test_forgot_password_link(driver):
    page = LoginPage(driver).load()
    page.click("forgot_password")
    assert "ForgotPassword" in driver.current_url


@pytest.mark.regression
def test_admin_login_link(driver):
    page = LoginPage(driver).load()
    page.click("admin_login")
    assert "AdminLogin" in driver.current_url


@pytest.mark.smoke
def test_logout(driver):
    page = LoginPage(driver).load()
    assert page.login_as_training_user()
    HomePage(driver).logout()
    assert page.is_visible("username", timeout=10), "After logout the login page should show"


# ---- Data driven login (DataProvider / Excel - Framework steps 17 and 18) ----
@pytest.mark.regression
@pytest.mark.parametrize("username,password,should_login", read_rows("test_data.xlsx", "login"))
def test_login_data_driven(driver, username, password, should_login):
    page = LoginPage(driver).load()
    page.login(username, password)
    if should_login.lower() == "yes":
        assert page.is_logged_in()
    else:
        time.sleep(2)
        assert page.is_on_login_page()
