"""Employee module - Create (10 tests) and Search (10 tests). One logged-in browser is shared."""
import random
import time

import pytest

from pages.employee_pages import EmployeeCreatePage, EmployeeSearchPage
from pages.home_page import HomePage
from utils.excel_reader import read_rows

pytestmark = pytest.mark.employee


def unique_mobile():
    """A made-up test number (90000 + 5 random digits). It is not anyone's real number."""
    return "90000" + "".join(random.choice("0123456789") for _ in range(5))


# ======================= Employee > Create =======================

@pytest.mark.smoke
def test_create_page_opens_from_menu(logged_in):
    HomePage(logged_in).load().go_to_employee_create()
    assert "Employee/Create" in logged_in.current_url


@pytest.mark.regression
def test_create_page_default_values(logged_in):
    page = EmployeeCreatePage(logged_in).load()
    assert page.find("male").is_selected(), "Male should be selected by default"
    assert page.selected_text("country") == "--Select Country--"
    assert not page.find("other_city").is_displayed(), "Other City box should be hidden at first"


@pytest.mark.regression
def test_create_required_field_messages(logged_in):
    page = EmployeeCreatePage(logged_in).load()
    page.save()
    time.sleep(1)
    errors = page.error_messages()
    for msg in ["Please enter first name.", "Please enter last name.",
                "Please enter email.", "Please enter mobile number."]:
        assert msg in errors, f"Missing message: {msg}"


@pytest.mark.regression
def test_create_invalid_email(logged_in):
    page = EmployeeCreatePage(logged_in).load()
    page.fill_form(first="Test", last="User", email="wrong-email", mobile=unique_mobile())
    page.save()
    time.sleep(1)
    assert "Please enter valid email address" in page.error_messages()


@pytest.mark.regression
def test_create_mobile_must_be_10_digits(logged_in):
    page = EmployeeCreatePage(logged_in).load()
    page.fill_form(first="Test", last="User", email="test@gmail.com", mobile="12345")
    page.save()
    time.sleep(1)
    assert "Mobile No must be 10 digits." in page.error_messages()


@pytest.mark.regression
def test_create_name_max_length_20(logged_in):
    page = EmployeeCreatePage(logged_in).load()
    page.type("first_name", "A" * 30)
    assert len(page.value_of("first_name")) == 20, "maxlength=20 should stop at 20 characters"


@pytest.mark.regression
def test_country_loads_cities(logged_in):
    page = EmployeeCreatePage(logged_in).load()
    page.select_by_text("country", "India")
    page.wait.until(lambda d: len(page._city_options()) > 1)
    assert len(page._city_options()) > 1, "Selecting a country should load its cities"


@pytest.mark.regression
def test_other_city_checkbox(logged_in):
    page = EmployeeCreatePage(logged_in).load()
    page.click("other_city_chk")
    assert page.find("other_city").is_displayed()
    assert not page.find("city").is_enabled(), "City dropdown should be disabled for Other City"


@pytest.mark.regression
def test_skill_checkboxes_listed(logged_in):
    page = EmployeeCreatePage(logged_in).load()
    names = page.skill_names()
    assert len(names) == 6
    for skill in ["AWS", "DevOps", "QA-Automation", "WebServices"]:
        assert skill in names


@pytest.mark.smoke
@pytest.mark.parametrize("first,last,email,gender,country,skill", read_rows("test_data.xlsx", "employee"))
def test_create_employee_success(logged_in, first, last, email, gender, country, skill):
    mobile = unique_mobile()
    # every run needs a new email - the site does not accept an email that already exists
    user, domain = email.split("@")
    email = f"{user}{mobile[-5:]}@{domain}"
    page = EmployeeCreatePage(logged_in).load()
    page.fill_form(first=first, last=last, email=email, mobile=mobile,
                   gender=gender, address="Hyderabad", country=country, skills=[skill])
    page.save()
    saved, message = page.wait_for_save_result()
    # Real check: the new employee must be found on the Search page by its mobile number
    found = EmployeeSearchPage(logged_in).load().mobile_exists(mobile)
    assert found, f"Employee with mobile {mobile} not found after Save. Message on screen: {message}"


# ======================= Employee > Search =======================

@pytest.mark.smoke
def test_search_page_opens_from_menu(logged_in):
    HomePage(logged_in).load().go_to_employee_search()
    assert "Employee/Search" in logged_in.current_url


@pytest.mark.regression
def test_search_table_headers(logged_in):
    page = EmployeeSearchPage(logged_in).load()
    expected = ["First Name", "Last Name", "Mobile No", "Email Id", "Gender",
                "Birth Date", "Country", "City", "Action"]
    assert page.header_names() == expected


@pytest.mark.regression
def test_search_shows_10_rows_per_page(logged_in):
    page = EmployeeSearchPage(logged_in).load()
    assert page.row_count() == 10


@pytest.mark.regression
def test_search_by_name(logged_in):
    page = EmployeeSearchPage(logged_in).load()
    name = page.first_names()[0]
    page.search(name=name)
    results = page.first_names()
    assert results and all(name.lower() in r.lower() for r in results)


@pytest.mark.regression
def test_search_by_mobile(logged_in):
    page = EmployeeSearchPage(logged_in).load()
    mobile = logged_in.find_element("xpath", "//table[@id='tblEmployee']/tbody/tr[1]/td[3]").text
    page.search(mobile=mobile)
    mobiles = [c.text for c in logged_in.find_elements("xpath", "//table[@id='tblEmployee']/tbody/tr/td[3]")]
    assert mobile in mobiles


@pytest.mark.regression
def test_search_no_results(logged_in):
    page = EmployeeSearchPage(logged_in).load()
    page.search(name="zzqqxx_no_such_name")
    names = [n for n in page.first_names() if n.strip()]
    # DataTables shows one row saying "No data available" when nothing matches
    assert all("zzqqxx" not in n for n in names)
    assert not any(n for n in names if "no data" not in n.lower()), f"Unexpected results: {names}"


@pytest.mark.regression
def test_clear_button(logged_in):
    page = EmployeeSearchPage(logged_in).load()
    page.type("name", "abc")
    page.click("clear")
    time.sleep(1)
    assert page.value_of("name") == ""


@pytest.mark.regression
def test_pagination_next(logged_in):
    page = EmployeeSearchPage(logged_in).load()
    first_page = page.first_names()
    page.click("next_page")
    time.sleep(2)
    assert page.first_names() != first_page, "Next should show different employees"


@pytest.mark.regression
def test_add_employee_button(logged_in):
    page = EmployeeSearchPage(logged_in).load()
    page.click("add_employee")
    assert "Employee/Create" in logged_in.current_url


@pytest.mark.regression
def test_delete_asks_for_confirmation(logged_in):
    """Only checks the confirmation popup and then cancels - does not delete anyone's data."""
    page = EmployeeSearchPage(logged_in).load()
    logged_in.find_element("xpath", "(//a[@title='Delete'])[1]").click()
    assert page.page_has_text("Are you sure you want to delete?")
    logged_in.find_element("xpath", "//button[contains(@class,'swal2-cancel') or normalize-space()='Cancel']").click()
