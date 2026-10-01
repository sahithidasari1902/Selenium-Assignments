"""
Assignment 2: Operations on Web Elements
Text box, radio button, check box, dropdown, links and XPath - on Magnus pages.

Run:  python ex2_web_elements.py
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from common import get_driver, login, open_page, step


def text_box(driver):
    step("TEXT BOX (Employee > Create)")
    open_page(driver, "Employee/Create")
    first = driver.find_element(By.ID, "FirstName")
    first.send_keys("Sahithi")                                               # 1. type
    print("1. Typed value           :", first.get_attribute("value"))        # 2. get value
    print("3. Placeholder           :", first.get_attribute("placeholder"))  # 3. placeholder
    first.clear()                                                             # 4. clear
    print("4. Value after clear()   : '" + first.get_attribute("value") + "'")
    print("5. Enabled?              :", first.is_enabled())                   # 5. enabled

    # City box becomes disabled when 'Other City' is ticked
    driver.find_element(By.XPATH, "//label[@for='chkOtherCity']").click()
    print("5. City dropdown enabled after ticking Other City:",
          driver.find_element(By.ID, "CityId").is_enabled())
    driver.find_element(By.XPATH, "//label[@for='chkOtherCity']").click()


def radio_buttons(driver):
    step("RADIO BUTTONS (Gender)")
    radios = driver.find_elements(By.NAME, "rdbGender")
    print("2. Number of radio buttons in group:", len(radios))
    print("3. All values:", [r.get_attribute("value") for r in radios])
    driver.find_element(By.XPATH, "//input[@name='rdbGender' and @value='F']").click()   # 1. select by value
    for r in radios:
        if r.is_selected():                                                               # 5. selected?
            label = r.find_element(By.XPATH, "./parent::*").text.strip()
            print("4. Selected radio value:", r.get_attribute("value"), "| label text:", label or "(label is next to it)")
    print("6. Female radio enabled:", driver.find_element(By.ID, "rdbFemale").is_enabled())


def check_boxes(driver):
    step("CHECK BOXES (Skills)")
    skills = driver.find_elements(By.CSS_SELECTOR, "input.chkSkill")
    print("Number of skill checkboxes:", len(skills))
    for cb in skills:
        label = cb.find_element(By.XPATH, "./parent::*").text.strip()
        print("  ", cb.get_attribute("id"), "->", label)
    # select by label text
    driver.find_element(By.XPATH, "//input[@class='chkSkill m-r-sm']/parent::*[contains(.,'QA-Automation')]//input").click()
    print("QA-Automation selected:", driver.find_element(By.ID, "chkSkill_1").is_selected())


def dropdown(driver):
    step("DROPDOWN (Country)")
    country = Select(driver.find_element(By.ID, "CountryId"))
    print("1. All options:", [o.text for o in country.options])
    print("2. First selected option:", country.first_selected_option.text)
    country.select_by_value("1")                                   # 3. by value
    print("3. After select_by_value('1')        :", country.first_selected_option.text)
    country.select_by_visible_text("USA")                          # 4. by visible text
    print("4. After select_by_visible_text('USA'):", country.first_selected_option.text)
    country.select_by_index(2)                                     # 5. by index
    print("5. After select_by_index(2)          :", country.first_selected_option.text)


def links(driver):
    step("LINKS (More > Links)")
    open_page(driver, "Home/Links")
    all_links = driver.find_elements(By.TAG_NAME, "a")
    print("3. Total links on the page:", len(all_links))
    for a in all_links[:10]:
        print("   ", repr(a.text), "->", a.get_attribute("href"))
    driver.find_element(By.PARTIAL_LINK_TEXT, "Image").click()      # 1. partial link text (opens the tab)
    print("1. Clicked partial link 'Image' -> Image Links tab")
    driver.find_element(By.LINK_TEXT, "Working Links").click()      # 2. link text
    print("2. Clicked link text 'Working Links'")
    driver.find_element(By.LINK_TEXT, "Image Links").click()
    img_link = driver.find_element(By.XPATH, "//img[contains(@src,'google-logo')]/parent::a")
    print("4. Image link points to:", img_link.get_attribute("href"), "(not clicked, it leaves the site)")


def xpath_examples(driver):
    step("XPATH (More > Links and Employee > Create)")
    open_page(driver, "Home/Links")
    link1 = driver.find_element(By.XPATH, "//a[text()='Link 1']")
    print("1. Label text and colour:", link1.text, "|", link1.value_of_css_property("color"))
    open_page(driver, "Employee/Create")
    print("2. id        :", driver.find_element(By.XPATH, "//input[@id='FirstName']").get_attribute("placeholder"))
    print("2. name      :", driver.find_element(By.XPATH, "//input[@name='LastName']").get_attribute("placeholder"))
    print("2. className :", driver.find_element(By.XPATH, "//h3[@class='box-title']").text)
    print("3. contains():", driver.find_element(By.XPATH, "//label[contains(text(),'Mobile')]").text)
    print("4. text()    :", driver.find_element(By.XPATH, "//label[text()='Email']").get_attribute("for"))
    print("5. starts-with():", driver.find_element(By.XPATH, "//input[starts-with(@id,'First')]").get_attribute("id"))
    print("6. following-sibling:", driver.find_element(By.XPATH, "//label[@for='FirstName']/following-sibling::input").get_attribute("id"))
    print("6. preceding-sibling:", driver.find_element(By.XPATH, "//input[@id='LastName']/preceding-sibling::label").text)
    print("7. parent    :", driver.find_element(By.XPATH, "//input[@id='EmailId']/parent::div").get_attribute("class"))
    print("7. ancestor  :", driver.find_element(By.XPATH, "//input[@id='EmailId']/ancestor::form").get_attribute("id"))
    print("7. child     :", driver.find_element(By.XPATH, "//select[@id='CountryId']/child::option[2]").text)
    print("7. descendant:", len(driver.find_elements(By.XPATH, "//form[@id='frmEmployee']/descendant::input")), "inputs in the form")
    print("8. AND       :", driver.find_element(By.XPATH, "//input[@type='radio' and @value='M']").get_attribute("id"))
    print("8. OR        :", len(driver.find_elements(By.XPATH, "//input[@id='FirstName' or @id='LastName']")), "elements")


if __name__ == "__main__":
    driver = get_driver()
    try:
        login(driver)
        text_box(driver)
        radio_buttons(driver)
        check_boxes(driver)
        dropdown(driver)
        links(driver)
        xpath_examples(driver)
    finally:
        driver.quit()
