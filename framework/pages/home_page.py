"""Home page and the side menu."""
from pages.base_page import BasePage


class HomePage(BasePage):
    SECTION = "home"

    MORE_PAGES = {
        "Multiple Tabs": "Home/Tabs", "Menu": "Home/Menu", "Autocomplete": "Home/AutoComplete",
        "Collapsible Content": "Home/Collapse", "Images": "Home/UploadImage", "Slider": "Home/Slider",
        "Tooltips": "Home/Tooltip", "Popups": "Home/Popup", "Links": "Home/Links",
        "CSS Properties": "Home/CssProperty", "iFrames": "Home/Iframe",
    }

    def load(self):
        self.open("Home/Index")
        return self

    def _click_employee_submenu(self, link_name):
        """Open the Employee menu once and click a sub-menu link.
        If the slow site has not finished opening the menu, click the link with JavaScript."""
        if not self.is_visible(link_name, timeout=1):
            self.click("employee_menu")
        if self.is_visible(link_name, timeout=5):
            self.click(link_name)
        else:
            self.log.warning("Menu did not open in time - clicking %s with JavaScript", link_name)
            self.driver.execute_script("arguments[0].click();", self.find(link_name))

    def go_to_employee_create(self):
        self._click_employee_submenu("create_link")

    def go_to_employee_search(self):
        self._click_employee_submenu("search_link")

    def open_more_item(self, link_text):
        self.click("more_menu")
        self.driver.find_element("link text", link_text).click()

    def logout(self):
        self.click("logout")
