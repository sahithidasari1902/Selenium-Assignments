"""Reads config.ini (constants) and locators.ini (web elements)."""
import configparser
import os

from selenium.webdriver.common.by import By

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_config = configparser.ConfigParser()
_config.read(os.path.join(ROOT, "config", "config.ini"))

_locators = configparser.ConfigParser(interpolation=None)
_locators.read(os.path.join(ROOT, "config", "locators.ini"))

_BY = {
    "id": By.ID, "name": By.NAME, "xpath": By.XPATH, "css": By.CSS_SELECTOR,
    "link": By.LINK_TEXT, "partial_link": By.PARTIAL_LINK_TEXT,
    "class": By.CLASS_NAME, "tag": By.TAG_NAME,
}


def get(section, key):
    return _config.get(section, key)


def locator(page, name):
    """Return a (By, value) tuple, e.g. locator('login', 'username') -> (By.ID, 'UserName')."""
    how, value = _locators.get(page, name).split(":", 1)
    return _BY[how.strip()], value.strip()
