"""More menu pages - 10 tests."""
import time

import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

pytestmark = pytest.mark.more


@pytest.fixture
def page(logged_in):
    return BasePage(logged_in)


@pytest.mark.regression
def test_tabs_switch_content(page):
    page.open("Home/Tabs")
    page.driver.find_element("link text", "UnLearning").click()
    time.sleep(0.5)
    assert page.driver.find_element("id", "tab_2").is_displayed()
    assert not page.driver.find_element("id", "tab_1").is_displayed()


@pytest.mark.regression
def test_menu_single_option_message(page):
    page.open("Home/Menu")
    page.driver.find_element("id", "b2").click()
    assert page.driver.find_element("id", "label").text == "You Have Selected Java Menu Option."


@pytest.mark.regression
def test_menu_sub_menu_hover(page):
    page.open("Home/Menu")
    page.driver.find_element("link text", "Sub Menus").click()
    ActionChains(page.driver).move_to_element(
        page.driver.find_element("xpath", "//a[@class='dropbtn' and text()='JAVA']")).perform()
    page.driver.find_element("id", "springbtn").click()
    assert "Spring" in page.driver.find_element("id", "label1").text


@pytest.mark.regression
def test_autocomplete_suggestions(page):
    page.open("Home/AutoComplete")
    page.driver.find_element("id", "txtSingleAutoComplete").send_keys("Py")
    items = page.wait.until(EC.visibility_of_all_elements_located(("css selector", "ul.ui-autocomplete li")))
    assert "Python" in [i.text for i in items]


@pytest.mark.regression
def test_collapse_expands_panel(page):
    page.open("Home/Collapse")
    page.driver.find_element("xpath", "//a[@href='#collapseOne']").click()
    page.wait.until(EC.visibility_of_element_located(("id", "collapseOne")))
    assert "in" in page.driver.find_element("id", "collapseOne").get_attribute("class").split() or \
        page.driver.find_element("id", "collapseOne").is_displayed()


@pytest.mark.regression
def test_slider_drag_changes_value(page):
    page.open("Home/Slider")
    before = page.driver.find_element("id", "ex6SliderVal").text
    handle = page.driver.find_element("css selector", ".slider-handle")
    ActionChains(page.driver).drag_and_drop_by_offset(handle, 80, 0).perform()
    assert page.driver.find_element("id", "ex6SliderVal").text != before


@pytest.mark.regression
def test_tooltip_text_changes_after_click(page):
    page.open("Home/Tooltip")
    btn = page.driver.find_element("id", "btnTooltip")
    btn.click()
    time.sleep(0.5)
    assert btn.get_attribute("data-original-title") == "Thank you for being here!"


@pytest.mark.smoke
def test_alert_box(page):
    page.open("Home/Popup")
    page.driver.find_element("id", "alertBox").click()
    alert = page.wait.until(EC.alert_is_present())
    assert alert.text == "This is an alert Box!"
    alert.accept()


@pytest.mark.regression
def test_prompt_box(page):
    page.open("Home/Popup")
    page.driver.find_element("id", "promptBtn").click()
    alert = page.wait.until(EC.alert_is_present())
    alert.send_keys("Sahithi")
    alert.accept()
    assert page.driver.find_element("id", "promptBox").text == "Sahithi"


@pytest.mark.regression
def test_iframe_two_shows_home_page(page):
    page.open("Home/Iframe")
    page.driver.switch_to.frame("iframe2")
    try:
        assert page.driver.find_elements("link text", "Employee"), "Frame Two should show the Magnus menu"
    finally:
        page.driver.switch_to.default_content()
