"""Creates the browser (Framework step 16: run the scripts in all browsers)."""
from selenium import webdriver


def create_driver(browser="chrome", headless=False):
    browser = browser.lower()
    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        driver = webdriver.Edge(options=options)
    else:
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1400,900")
        driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.set_page_load_timeout(60)     # the Magnus site can be slow
    return driver
