"""
Step 1 of the Selenium assignment: explore the Magnus application.

This script opens Chrome, logs in to http://magnus.jalatechnologies.com with the
training account from the JALA email, visits every page it can find in the menu,
and saves the HTML and a screenshot of each page into the 'magnus_pages' folder.
Those saved pages are used to find the element locators for the test scripts.

How to run (Command Prompt, inside this folder):
    pip install selenium
    python explore_magnus.py
"""
import os
import re
import time
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://magnus.jalatechnologies.com/"
USERNAME = "training@jalaacademy.com"   # training account given in the JALA email
PASSWORD = "jobprogram"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "magnus_pages")
MAX_PAGES = 80


def safe_name(url, index):
    path = urlparse(url).path.strip("/") or "home"
    query = urlparse(url).query
    name = re.sub(r"[^A-Za-z0-9]+", "_", path + ("_" + query if query else ""))
    return f"{index:02d}_{name[:60]}"


def save_page(driver, name):
    with open(os.path.join(OUT_DIR, name + ".html"), "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    driver.save_screenshot(os.path.join(OUT_DIR, name + ".png"))
    print("  saved", name)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    driver = webdriver.Chrome()          # Selenium 4 downloads the right ChromeDriver automatically
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    try:
        # ---- Login page ----
        driver.get(BASE_URL)
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        save_page(driver, "00_login")

        email_box = driver.find_element(By.XPATH, "(//input[@type='email' or @type='text'])[1]")
        pwd_box = driver.find_element(By.XPATH, "//input[@type='password']")
        email_box.clear(); email_box.send_keys(USERNAME)
        pwd_box.clear(); pwd_box.send_keys(PASSWORD)
        driver.find_element(By.XPATH,
            "//button[contains(normalize-space(.),'Sign In')] | //input[@type='submit' or @value='Sign In']").click()

        wait.until(lambda d: "login" not in d.current_url.lower() or
                   len(d.find_elements(By.XPATH, "//input[@type='password']")) == 0)
        time.sleep(2)
        print("Logged in. Current page:", driver.current_url)

        # ---- Visit every internal link ----
        to_visit = [driver.current_url]
        seen = set()
        index = 1
        while to_visit and index <= MAX_PAGES:
            url = to_visit.pop(0).split("#")[0]
            if url in seen or urlparse(url).hostname != urlparse(BASE_URL).hostname:
                continue
            if any(word in url.lower() for word in ("logout", "logoff", "signout", "delete")):
                continue                     # never click logout or delete links
            seen.add(url)
            driver.get(url)
            time.sleep(1.5)
            save_page(driver, safe_name(url, index))
            index += 1
            for a in driver.find_elements(By.TAG_NAME, "a"):
                href = a.get_attribute("href")
                if href and not href.startswith("javascript"):
                    full = urljoin(driver.current_url, href).split("#")[0]
                    if full not in seen and full not in to_visit:
                        to_visit.append(full)

        print(f"\nDone. {index - 1} pages saved in: {OUT_DIR}")
        print("Tell Claude it finished so the pages can be read.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
