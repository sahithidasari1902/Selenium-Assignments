"""Employee > Create and Employee > Search pages."""
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from pages.base_page import BasePage


class EmployeeCreatePage(BasePage):
    SECTION = "employee_create"

    def load(self):
        self.open("Employee/Create")
        self.find("first_name")
        return self

    def fill_form(self, first="", last="", email="", mobile="", gender="M",
                  address="", country="", city="", skills=()):
        if first:
            self.type("first_name", first)
        if last:
            self.type("last_name", last)
        if email:
            self.type("email", email)
        if mobile:
            self.type("mobile", mobile)
        self.click("female" if gender == "F" else "male")
        if address:
            self.type("address", address)
        if country:
            self.select_by_text("country", country)
            # cities are loaded by Ajax after the country changes; a city must be chosen too
            self.wait.until(lambda d: len(self._city_options()) > 1)
            if city:
                self.select_by_text("city", city)
            else:
                Select(self.find("city")).select_by_index(1)     # first real city
                self.log.info("Select city '%s'", self.selected_text("city"))
        for skill in skills:
            self.driver.find_element(
                "xpath", f"//input[contains(@class,'chkSkill')]/parent::*[contains(normalize-space(.),'{skill}')]//input"
            ).click()

    def _city_options(self):
        return self.find("city").find_elements("tag name", "option")

    def save(self):
        self.click("save")

    def wait_for_save_result(self, timeout=10):
        """After Save the site shows 'Employee details saved successfully' and then opens the
        Search page. Returns (saved, message) where message is any popup/validation text seen."""
        end = time.time() + timeout
        seen = ""
        while time.time() < end:
            if "Employee/Search" in self.driver.current_url:
                return True, "redirected to Employee Search"
            popups = self.driver.find_elements(
                "xpath", "//*[contains(@class,'toast') or contains(@class,'field-validation-error') "
                         "or contains(@class,'alert') or contains(@class,'swal') or contains(@class,'noty') "
                         "or contains(text(),'already') or contains(text(),'exist') or contains(text(),'successfully')]")
            texts = []
            for p in popups:
                try:
                    if p.is_displayed() and p.text.strip():
                        texts.append(p.text.strip()[:120])
                except Exception:
                    pass
            if texts:
                seen = " | ".join(texts)
                if "saved successfully" in seen:
                    return True, seen
            time.sleep(0.5)
        return False, seen or "no message shown"

    def error_messages(self):
        return [e.text for e in self.find_all("field_errors") if e.text.strip()]

    def skill_names(self):
        return [cb.find_element("xpath", "./parent::*").text.strip() for cb in self.find_all("skills")]


class EmployeeSearchPage(BasePage):
    SECTION = "employee_search"

    def load(self):
        self.open("Employee/Search")
        self.wait_for_rows()
        return self

    def wait_for_rows(self):
        self.wait.until(EC.presence_of_element_located(self.loc("first_cells")))

    def search(self, name="", mobile=""):
        self.type("name", name)
        self.type("mobile", mobile)
        old_cells = self.find_all("first_cells")
        self.click("search")
        # wait for the grid to reload (old rows disappear), then give the new rows a moment
        if old_cells:
            try:
                WebDriverWait(self.driver, 10).until(EC.staleness_of(old_cells[0]))
            except Exception:
                pass
        time.sleep(1)

    def mobile_exists(self, mobile):
        """Search by mobile number and return True if that employee is in the grid."""
        self.search(mobile=mobile)
        cells = self.driver.find_elements("xpath", "//table[@id='tblEmployee']/tbody/tr/td[3]")
        return any(c.text.strip() == mobile for c in cells)

    def first_names(self):
        return [c.text for c in self.find_all("first_cells")]

    def row_count(self):
        return len(self.find_all("rows"))

    def header_names(self):
        return [h.text for h in self.find_all("headers")]
