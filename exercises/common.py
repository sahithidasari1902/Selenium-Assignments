"""Shared helpers for the exercise scripts (each script can be run on its own)."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://magnus.jalatechnologies.com/"
USERNAME = "training@jalaacademy.com"   # training account from the JALA email
PASSWORD = "jobprogram"


def get_driver():
    """Open Chrome. Selenium 4 downloads the matching ChromeDriver automatically."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.set_page_load_timeout(60)     # the Magnus site can be slow
    driver.implicitly_wait(5)
    return driver


def safe_get(driver, url, tries=3):
    """driver.get() that tries again if the site is slow to respond (connection time-out)."""
    import time
    for attempt in range(1, tries + 1):
        try:
            driver.get(url)
            return
        except Exception as err:
            if attempt == tries:
                raise
            print(f"  (page did not load: {str(err).splitlines()[0][:60]}... retrying {attempt}/{tries - 1})")
            time.sleep(3)


def open_login_page(driver):
    """Open the login page logged OUT, and wait for the page's own auto-fill to finish.
    The Magnus login page fills in the training username/password by itself shortly
    after loading, so tests that clear or type into the boxes must wait for that first."""
    import time
    safe_get(driver, BASE_URL)
    driver.delete_all_cookies()          # make sure we are logged out
    safe_get(driver, BASE_URL)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "UserName")))
    try:
        WebDriverWait(driver, 3).until(
            lambda d: d.find_element(By.ID, "UserName").get_attribute("value") != "")
    except Exception:
        pass
    time.sleep(0.5)


def login(driver):
    """Log in to Magnus and wait for the home page."""
    open_login_page(driver)
    driver.find_element(By.ID, "UserName").clear()
    driver.find_element(By.ID, "UserName").send_keys(USERNAME)
    driver.find_element(By.ID, "Password").clear()
    driver.find_element(By.ID, "Password").send_keys(PASSWORD)
    driver.find_element(By.ID, "btnLogin").click()
    WebDriverWait(driver, 40).until(EC.url_contains("/Home/Index"))


def open_page(driver, path):
    """Go straight to a page after logging in, e.g. open_page(driver, 'Home/Popup')."""
    safe_get(driver, BASE_URL + path)


def step(title):
    print("\n" + "=" * 60 + "\n" + title + "\n" + "=" * 60)
