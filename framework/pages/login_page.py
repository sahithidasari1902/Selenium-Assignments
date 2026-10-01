"""Login page: PageObjects come from [login] in locators.ini, PageActions are the methods below."""
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils import config_reader as cfg


class LoginPage(BasePage):
    SECTION = "login"

    def load(self):
        """Open the login page logged out and wait for its auto-fill to finish.
        (The page fills in the training credentials by itself shortly after loading.)"""
        self.open("")
        self.driver.delete_all_cookies()
        self.open("")
        self.find("username")
        try:
            WebDriverWait(self.driver, 3).until(
                lambda d: self.find("username").get_attribute("value") != "")
        except Exception:
            pass
        time.sleep(0.5)
        return self

    def login(self, username, password):
        self.type("username", username)
        self.type("password", password)
        self.click("sign_in")

    def login_as_training_user(self, tries=2):
        """Log in with the training account. The site can be slow, so wait up to 30s and retry once."""
        for attempt in range(1, tries + 1):
            self.login(cfg.get("app", "username"), cfg.get("app", "password"))
            if self.is_logged_in(timeout=30):
                return True
            self.log.warning("Login did not finish in time - retry %d", attempt)
            self.load()
        return False

    def is_logged_in(self, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains("/Home/Index"))
            return True
        except Exception:
            return False

    def is_on_login_page(self):
        return len(self.find_all("username")) > 0 and "/Home/Index" not in self.driver.current_url
