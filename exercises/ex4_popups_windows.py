"""
Assignment 4: Popups / Alerts and Windows (More > Popups and More > iFrames)

Run:  python ex4_popups_windows.py
"""
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common import get_driver, login, open_page, step


def alerts(driver):
    wait = WebDriverWait(driver, 10)
    open_page(driver, "Home/Popup")

    step("1 + 4. Alert box: read the message with .text and accept()")
    driver.find_element(By.ID, "alertBox").click()
    alert = wait.until(EC.alert_is_present())            # 10. switch_to.alert
    print("Alert message:", alert.text)
    alert.accept()
    print("Clicked OK (accept)")

    step("3 + 5. Confirm box: OK and Cancel")
    driver.find_element(By.ID, "confirmBox").click()
    confirm = wait.until(EC.alert_is_present())
    print("Confirm message:", confirm.text)
    confirm.dismiss()
    print("Clicked Cancel (dismiss)")
    driver.find_element(By.ID, "confirmBox").click()
    wait.until(EC.alert_is_present()).accept()
    print("Clicked OK (accept) on second try")

    step("2. Prompt box: type text and accept")
    driver.find_element(By.ID, "promptBtn").click()
    prompt = wait.until(EC.alert_is_present())
    print("Prompt message:", prompt.text)
    prompt.send_keys("Sahithi Dasari")
    prompt.accept()
    time.sleep(0.5)
    print("Page shows:", driver.find_element(By.ID, "promptBox").text)

    step("In-window (modal) popup - not a browser alert, so handled like normal elements")
    driver.find_element(By.ID, "btn-six").click()
    modal_title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#myModal1 .modal-title")))
    print("Modal title:", modal_title.text)
    driver.find_element(By.CSS_SELECTOR, "#myModal1 .btn-danger").click()
    wait.until(EC.invisibility_of_element_located((By.ID, "myModal1")))
    print("Modal closed")


def windows(driver):
    wait = WebDriverWait(driver, 10)
    open_page(driver, "Home/Popup")

    step("6. Single window: get the current window handle")
    main_window = driver.current_window_handle
    print("Main window handle:", main_window)

    step("7 + 8. Multiple windows: open popups and switch between them")
    driver.find_element(By.ID, "btn-one").click()
    driver.find_element(By.ID, "btn-two").click()
    wait.until(lambda d: len(d.window_handles) >= 3)
    handles = driver.window_handles
    print("Open windows:", len(handles))
    for h in handles:
        driver.switch_to.window(h)
        print("  ", h[:12], "->", driver.title[:50] or "(loading)", "|", driver.current_url[:60])
    for h in handles:                         # close every popup, keep the main window
        if h != main_window:
            driver.switch_to.window(h)
            driver.close()
    driver.switch_to.window(main_window)
    print("Back on main window:", driver.title)


def frames(driver):
    step("9. Switch to a frame (More > iFrames)")
    open_page(driver, "Home/Iframe")
    driver.switch_to.frame("iframe2")         # by id - Frame Two shows the Magnus home page
    print("Inside iframe2, first link text:", driver.find_element(By.TAG_NAME, "a").text)
    driver.switch_to.default_content()        # back to the main page
    print("Back in main page, heading:", driver.find_element(By.TAG_NAME, "h1").text)
    frame_el = driver.find_element(By.ID, "iframe1")
    driver.switch_to.frame(frame_el)           # by WebElement
    print("Switched into iframe1 by WebElement")
    driver.switch_to.default_content()
    driver.switch_to.frame(1)                  # by index (0-based)
    print("Switched into the 2nd frame by index")
    driver.switch_to.default_content()


if __name__ == "__main__":
    driver = get_driver()
    try:
        login(driver)
        alerts(driver)
        windows(driver)
        frames(driver)
    finally:
        driver.quit()
