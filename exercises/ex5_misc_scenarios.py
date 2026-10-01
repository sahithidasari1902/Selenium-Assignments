"""
Assignment 5: Selenium Miscellaneous Scenarios

Run:  python ex5_misc_scenarios.py
"""
import os
import time
import urllib.request
from urllib.error import HTTPError, URLError

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common import get_driver, login, open_page, step

SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")


def screenshot(driver):
    step("1. Capture screenshots")
    os.makedirs(SHOTS, exist_ok=True)
    open_page(driver, "Home/Index")
    full = os.path.join(SHOTS, "home_page.png")
    driver.save_screenshot(full)                                        # whole visible page
    driver.find_element(By.CLASS_NAME, "main-sidebar").screenshot(os.path.join(SHOTS, "sidebar_only.png"))  # one element
    print("Saved:", full, "and sidebar_only.png")


def iframe_click(driver):
    step("2. Click an element inside an iFrame")
    open_page(driver, "Home/Iframe")
    driver.switch_to.frame("iframe2")
    driver.find_element(By.LINK_TEXT, "Employee").click()
    print("Clicked 'Employee' inside iframe2")
    driver.switch_to.default_content()


def broken_links(driver):
    step("3. Find broken links (More > Links)")
    open_page(driver, "Home/Links")
    hrefs = {a.get_attribute("href") for a in driver.find_elements(By.CSS_SELECTOR, ".tab-content a")}
    for href in sorted(h for h in hrefs if h and h.startswith("http")):
        try:
            req = urllib.request.Request(href, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
            code = urllib.request.urlopen(req, timeout=10).status
        except HTTPError as e:
            code = e.code
        except (URLError, OSError) as e:
            code = "ERROR (" + str(getattr(e, "reason", e))[:40] + ")"
        broken = not isinstance(code, int) or code >= 400
        print(("BROKEN " if broken else "OK     "), code, href)


def waits(driver):
    step("4. Implicit and explicit waits")
    driver.implicitly_wait(5)            # implicit: every find_element waits up to 5s
    print("Implicit wait set to 5 seconds")
    open_page(driver, "Home/Tooltip")
    wait = WebDriverWait(driver, 10)     # explicit: wait for ONE specific condition
    button = wait.until(EC.element_to_be_clickable((By.ID, "btnTooltip")))
    print("Explicit wait: button is clickable ->", button.text)


def actions(driver):
    step("5. Actions class")
    act = ActionChains(driver)

    # Mouse hover (move_to_element) - More > Menu, Sub Menus tab
    open_page(driver, "Home/Menu")
    driver.find_element(By.LINK_TEXT, "Sub Menus").click()
    testing_menu = driver.find_element(By.XPATH, "//a[@class='dropbtn' and text()='Testing']")
    act.move_to_element(testing_menu).perform()
    time.sleep(0.5)
    driver.find_element(By.ID, "selbtn").click()
    print("Mouse hover + click sub menu ->", driver.find_element(By.ID, "label1").text)

    # Double click - Tooltip button
    open_page(driver, "Home/Tooltip")
    btn = driver.find_element(By.ID, "btnTooltip")
    ActionChains(driver).double_click(btn).perform()
    print("Double click on the tooltip button done. Tooltip:", btn.get_attribute("data-original-title"))

    # Click and hold + drag (slider handle) - More > Slider
    open_page(driver, "Home/Slider")
    handle = driver.find_element(By.CSS_SELECTOR, ".slider-handle")
    before = driver.find_element(By.ID, "ex6SliderVal").text
    ActionChains(driver).click_and_hold(handle).move_by_offset(60, 0).release().perform()
    print("Click and hold, drag slider:", before, "->", driver.find_element(By.ID, "ex6SliderVal").text)
    ActionChains(driver).drag_and_drop_by_offset(handle, -40, 0).perform()
    print("drag_and_drop_by_offset    :", driver.find_element(By.ID, "ex6SliderVal").text)

    # Keyboard: type with SHIFT and press ENTER - Employee > Search
    open_page(driver, "Employee/Search")
    name_box = driver.find_element(By.ID, "Name")
    ActionChains(driver).click(name_box).key_down(Keys.SHIFT).send_keys("a").key_up(Keys.SHIFT).perform()
    print("Typed with SHIFT held ->", name_box.get_attribute("value"))
    name_box.send_keys(Keys.ENTER)      # the page searches when Enter is pressed
    print("Pressed ENTER to search")


def web_table(driver):
    step("6. Web table (Employee > Search)")
    open_page(driver, "Employee/Search")
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id='tblEmployee']/tbody/tr/td")))
    rows = driver.find_elements(By.XPATH, "//table[@id='tblEmployee']/tbody/tr")
    cols = driver.find_elements(By.XPATH, "//table[@id='tblEmployee']/thead/tr/th")
    print("Row count:", len(rows), "| Column count:", len(cols))
    print("Cell (row 1, column 'Email Id'):",
          driver.find_element(By.XPATH, "//table[@id='tblEmployee']/tbody/tr[1]/td[4]").text)
    # Dynamic handling: find the row for a name, whatever row it is on
    first_name = driver.find_element(By.XPATH, "//table[@id='tblEmployee']/tbody/tr[1]/td[1]").text
    mobile = driver.find_element(By.XPATH,
        f"//table[@id='tblEmployee']//td[text()='{first_name}']/following-sibling::td[2]").text
    print(f"Dynamic lookup: mobile number of '{first_name}' is {mobile}")
    print("Total pages in the grid:", driver.find_element(By.ID, "spanTotalPages_EmployeeGrid").text)


def autocomplete(driver):
    step("7. Ajax auto-suggestion (More > Autocomplete)")
    open_page(driver, "Home/AutoComplete")
    box = driver.find_element(By.ID, "txtSingleAutoComplete")
    box.send_keys("ja")
    wait = WebDriverWait(driver, 10)
    suggestions = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "ul.ui-autocomplete li")))
    print("Suggestions:", [s.text for s in suggestions])
    for s in suggestions:
        if s.text == "JavaScript":
            s.click()
            break
    print("Selected value:", box.get_attribute("value"))


def calendar(driver):
    step("8. Select a date from the calendar (Employee > Create > Date Of Birth)")
    open_page(driver, "Employee/Create")
    dob = driver.find_element(By.ID, "DOB")
    dob.click()
    wait = WebDriverWait(driver, 10)
    try:
        days = wait.until(EC.visibility_of_all_elements_located(
            (By.XPATH, "//div[contains(@class,'datepicker')]//td[contains(@class,'day') "
                       "and not(contains(@class,'old')) and not(contains(@class,'new'))]")))
        for d in days:
            if d.text == "15":
                d.click()
                break
        print("Picked day 15 from the calendar ->", dob.get_attribute("value"))
    except Exception:
        dob.send_keys("15/08/1998")
        print("Calendar widget not found, typed the date instead ->", dob.get_attribute("value"))


def cookies_and_profile(driver):
    step("9. Cookies and browser profile")
    open_page(driver, "Home/Index")
    print("Cookies now:", [c["name"] for c in driver.get_cookies()])
    driver.add_cookie({"name": "jala_test", "value": "sahithi"})
    print("After add_cookie   :", driver.get_cookie("jala_test"))
    driver.delete_cookie("jala_test")
    print("After delete_cookie:", driver.get_cookie("jala_test"))
    print("delete_all_cookies() would log you out, so it is only shown here.")

    # Browser profile / options: start Chrome with custom settings
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--window-size=1000,700")
    options.add_argument("--disable-notifications")
    profile_driver = webdriver.Chrome(options=options)
    profile_driver.get("https://magnus.jalatechnologies.com/")
    print("Second browser with custom options (incognito, 1000x700):", profile_driver.get_window_size())
    profile_driver.quit()


if __name__ == "__main__":
    driver = get_driver()
    try:
        login(driver)
        screenshot(driver)
        iframe_click(driver)
        broken_links(driver)
        waits(driver)
        actions(driver)
        web_table(driver)
        autocomplete(driver)
        calendar(driver)
        cookies_and_profile(driver)
    finally:
        driver.quit()
