"""
Assignment 1: Selenium Locators - Magnus Login page

Part A: identify the login page elements using all 8 locator types.
Part B: 5 automation scripts for the login page.

Run:  python ex1_locators.py
"""
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common import BASE_URL, PASSWORD, USERNAME, get_driver, open_login_page, step


def part_a_locators(driver):
    step("PART A: Identify login page elements with every locator type")
    open_login_page(driver)

    by_id = driver.find_element(By.ID, "UserName")                                  # 1. ID
    by_name = driver.find_element(By.NAME, "Password")                              # 2. NAME
    by_class = driver.find_element(By.CLASS_NAME, "btn-primary")                    # 3. CLASS_NAME
    by_tag = driver.find_elements(By.TAG_NAME, "input")                             # 4. TAG_NAME
    by_link = driver.find_element(By.LINK_TEXT, "Forgot Password")                  # 5. LINK_TEXT
    by_partial = driver.find_element(By.PARTIAL_LINK_TEXT, "Admin")                 # 6. PARTIAL_LINK_TEXT
    by_css = driver.find_element(By.CSS_SELECTOR, "input#UserName.form-control")    # 7. CSS_SELECTOR
    by_xpath = driver.find_element(By.XPATH, "//button[@id='btnLogin']")            # 8. XPATH

    print("ID              -> placeholder:", by_id.get_attribute("placeholder"))
    print("NAME            -> type:", by_name.get_attribute("type"))
    print("CLASS_NAME      -> text:", by_class.text)
    print("TAG_NAME        -> number of <input> tags:", len(by_tag))
    print("LINK_TEXT       -> href:", by_link.get_attribute("href"))
    print("PARTIAL_LINK    -> text:", by_partial.text)
    print("CSS_SELECTOR    -> id:", by_css.get_attribute("id"))
    print("XPATH           -> text:", by_xpath.text)

    # A few more XPath / CSS styles for the same elements
    print("XPath by placeholder :", driver.find_element(By.XPATH, "//input[@placeholder='Password']").get_attribute("id"))
    print("XPath contains()     :", driver.find_element(By.XPATH, "//a[contains(text(),'Forgot')]").text)
    print("CSS attribute        :", driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']").get_attribute("id"))


def script1_valid_login(driver):
    step("Script 1: Valid login goes to the Home page")
    open_login_page(driver)
    driver.find_element(By.ID, "UserName").clear()
    driver.find_element(By.ID, "UserName").send_keys(USERNAME)
    driver.find_element(By.ID, "Password").clear()
    driver.find_element(By.ID, "Password").send_keys(PASSWORD)
    driver.find_element(By.ID, "btnLogin").click()
    WebDriverWait(driver, 15).until(EC.url_contains("/Home/Index"))
    print("PASS - landed on", driver.current_url, "| title:", driver.title)
    driver.find_element(By.LINK_TEXT, "Logout").click()          # log out for the next scripts
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "UserName")))


def script2_invalid_password(driver):
    step("Script 2: Wrong password stays on the login page")
    open_login_page(driver)
    driver.find_element(By.ID, "UserName").clear()
    driver.find_element(By.ID, "UserName").send_keys(USERNAME)
    driver.find_element(By.ID, "Password").clear()
    driver.find_element(By.ID, "Password").send_keys("wrongpass123")
    driver.find_element(By.ID, "btnLogin").click()
    time.sleep(3)
    still_on_login = len(driver.find_elements(By.ID, "UserName")) > 0 and "/Home/Index" not in driver.current_url
    print("PASS" if still_on_login else "FAIL", "- still on login page:", still_on_login)


def script3_empty_fields(driver):
    step("Script 3: Empty username and password show validation messages")
    open_login_page(driver)
    # Empty both boxes right before clicking, so the page's auto-fill cannot put the values back
    driver.execute_script("document.getElementById('UserName').value='';"
                          "document.getElementById('Password').value='';")
    driver.find_element(By.ID, "btnLogin").click()
    wait = WebDriverWait(driver, 5)
    try:
        wait.until(lambda d: d.find_elements(By.XPATH,
            "//*[contains(text(),'Please enter email or mobile no.') or "
            "contains(text(),'Please fill all the required field')]"))
    except Exception:
        pass
    user_msg = driver.find_elements(By.XPATH, "//*[contains(text(),'Please enter email or mobile no.')]")
    pwd_msg = driver.find_elements(By.XPATH, "//*[contains(text(),'Please enter password.')]")
    toast = driver.find_elements(By.XPATH, "//*[contains(text(),'Please fill all the required field')]")
    print("Username message:", bool(user_msg), "| Password message:", bool(pwd_msg),
          "| Popup 'Please fill all the required field':", bool(toast))
    print("Still on login page:", "/Home/Index" not in driver.current_url)
    print("PASS" if (user_msg or toast) and "/Home/Index" not in driver.current_url else "FAIL")


def script4_remember_me(driver):
    step("Script 4: Remember Me checkbox can be ticked")
    open_login_page(driver)
    checkbox = driver.find_element(By.ID, "RememberMe")
    label = driver.find_element(By.XPATH, "//label[@for='RememberMe']")
    print("Selected before click:", checkbox.is_selected())
    label.click()          # the real checkbox is styled, so click its label
    if not checkbox.is_selected():
        driver.execute_script("arguments[0].click();", checkbox)   # JavaScript click as a fallback
    print("Selected after click :", checkbox.is_selected())
    print("PASS" if checkbox.is_selected() else "FAIL")


def script5_links(driver):
    step("Script 5: Forgot Password and Admin Login links open the right pages")
    open_login_page(driver)
    driver.find_element(By.LINK_TEXT, "Forgot Password").click()
    print("Forgot Password URL:", driver.current_url,
          "->", "PASS" if "ForgotPassword" in driver.current_url else "FAIL")
    open_login_page(driver)
    driver.find_element(By.PARTIAL_LINK_TEXT, "Admin").click()
    print("Admin Login URL    :", driver.current_url,
          "->", "PASS" if "AdminLogin" in driver.current_url else "FAIL")


if __name__ == "__main__":
    driver = get_driver()
    try:
        part_a_locators(driver)
        script1_valid_login(driver)
        script2_invalid_password(driver)
        script3_empty_fields(driver)
        script4_remember_me(driver)
        script5_links(driver)
    finally:
        driver.quit()
