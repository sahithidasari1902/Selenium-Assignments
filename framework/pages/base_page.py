"""BasePage: common actions every page uses (click, type, wait, read text)."""
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from utils import config_reader as cfg
from utils.logger import get_logger


class BasePage:
    SECTION = ""          # section name in locators.ini, set by each page

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, int(cfg.get("run", "explicit_wait")))
        self.log = get_logger(self.__class__.__name__)
        self.base_url = cfg.get("app", "base_url")

    # ---- locator lookup (web elements come from locators.ini) ----
    def loc(self, name, section=None):
        return cfg.locator(section or self.SECTION, name)

    def find(self, name):
        return self.wait.until(EC.presence_of_element_located(self.loc(name)))

    def find_all(self, name):
        return self.driver.find_elements(*self.loc(name))

    # ---- actions ----
    def open(self, path="", tries=3):
        """Open a page. If the site is slow and the load times out, wait and try again."""
        url = self.base_url + path
        for attempt in range(1, tries + 1):
            self.log.info("Open %s", url)
            try:
                self.driver.get(url)
                return
            except Exception as err:
                if attempt == tries:
                    raise
                self.log.warning("Page did not load (%s) - retry %d", str(err).splitlines()[0][:60], attempt)
                time.sleep(3)

    def click(self, name):
        self.log.info("Click %s", name)
        self.wait.until(EC.element_to_be_clickable(self.loc(name))).click()

    def type(self, name, text):
        self.log.info("Type '%s' into %s", text, name)
        el = self.find(name)
        el.clear()
        el.send_keys(text)

    def text_of(self, name):
        return self.find(name).text

    def value_of(self, name):
        return self.find(name).get_attribute("value")

    def is_visible(self, name, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.loc(name)))
            return True
        except Exception:
            return False

    def select_by_text(self, name, text):
        self.log.info("Select '%s' in %s", text, name)
        Select(self.find(name)).select_by_visible_text(text)

    def selected_text(self, name):
        return Select(self.find(name)).first_selected_option.text

    def page_has_text(self, text, timeout=10):
        """Wait until some visible element contains the text (used for toast messages)."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(("xpath", f"//*[contains(text(),\"{text}\")]")))
            return True
        except Exception:
            return False
