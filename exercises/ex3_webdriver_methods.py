"""
Assignment 3: WebDriver Methods (Python names shown next to the Java names)

Run:  python ex3_webdriver_methods.py
"""
import time

from selenium.webdriver.common.by import By

from common import BASE_URL, get_driver, login, step


def main():
    driver = get_driver()
    try:
        login(driver)

        step("Browser / page methods")
        driver.get(BASE_URL + "Home/Index")                                        # get()
        print("current_url      (getCurrentUrl) :", driver.current_url)
        print("title            (getTitle)      :", driver.title)
        print("page_source      (getPageSource) :", len(driver.page_source), "characters")

        step("Finding elements")
        menu = driver.find_element(By.LINK_TEXT, "Employee")                       # findElement()
        links = driver.find_elements(By.TAG_NAME, "a")                             # findElements()
        print("find_element  -> tag_name (getTagName):", menu.tag_name, "| text (getText):", menu.text)
        print("find_elements -> number of links:", len(links))

        step("Windows and switchTo")
        print("current_window_handle (getWindowHandle) :", driver.current_window_handle)
        print("window_handles        (getWindowHandles):", driver.window_handles)
        driver.switch_to.new_window("tab")                                          # switchTo()
        driver.get(BASE_URL + "Home/Tabs")
        print("Opened a new tab ->", driver.title, "| handles now:", len(driver.window_handles))
        driver.close()                                                              # close() - closes ONE tab
        driver.switch_to.window(driver.window_handles[0])
        print("close() closed the new tab, back to:", driver.title)

        step("manage() - window, timeouts, cookies")
        driver.set_window_size(1200, 800)
        print("Window size after set_window_size:", driver.get_window_size())
        driver.maximize_window()
        driver.implicitly_wait(5)
        print("Number of cookies:", len(driver.get_cookies()))

        step("navigate()")
        driver.get(BASE_URL + "Employee/Create")                                    # navigate().to()
        print("to()      ->", driver.title)
        driver.back()                                                               # navigate().back()
        print("back()    ->", driver.title)
        driver.forward()                                                            # navigate().forward()
        print("forward() ->", driver.title)
        driver.refresh()                                                            # navigate().refresh()
        print("refresh() ->", driver.title)

        step("Element methods")
        first = driver.find_element(By.ID, "FirstName")
        first.send_keys("JALA")                                                     # sendKeys()
        print("get_attribute('value')    :", first.get_attribute("value"))         # getAttribute()
        print("is_displayed (isDisplayed):", first.is_displayed())
        print("is_enabled   (isEnabled)  :", first.is_enabled())
        male = driver.find_element(By.ID, "rdbMale")
        print("is_selected  (isSelected) : Male radio =", male.is_selected())
        print("size         (getSize)    :", first.size)
        print("location     (getLocation):", first.location)
        driver.find_element(By.ID, "rdbFemale").click()                             # click()
        print("click() on Female -> selected:", driver.find_element(By.ID, "rdbFemale").is_selected())

        step("Thread.sleep equivalent")
        time.sleep(2)                                                               # Thread.sleep(2000)
        print("time.sleep(2) paused for 2 seconds (use explicit waits instead in real tests)")
    finally:
        driver.quit()                                                               # quit() - closes ALL windows
        print("\nquit() closed the browser and ended the session.")


if __name__ == "__main__":
    main()
