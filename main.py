import time
from selenium import webdriver
from selenium.common import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import schedule

userID = "Enter here"  # Enter username
password = "Enter here"  # Enter password
browser = webdriver.Chrome()
browser.get('https://wish.wis.ntu.edu.sg/pls/webexe/ldap_login.login?w_url=https://wish.wis.ntu.edu.sg/pls/webexe'
            '/aus_stars_planner.main')

userUI = browser.find_element(By.ID, 'UID')
userUI.send_keys(userID)
browser.find_element(By.XPATH, "//input[@type='submit']").click()

passUI = browser.find_element(By.ID, 'PW')
passUI.send_keys(password)


def register_course():
    browser.find_element(By.XPATH, "//input[@type='submit']").click()

    registerAllowed = False
    while not registerAllowed:
        submit_present = ec.presence_of_element_located(
            (By.XPATH, "//input[@type='submit' and @value='Add (Register) Selected Course(s)']"))
        WebDriverWait(browser, 0).until(submit_present)
        browser.find_element(By.XPATH,
                             "//input[@type='submit' and @value='Add (Register) Selected Course(s)']").click()
        try:
            alert = browser.switch_to.alert
            if alert.text.find('not allowed to register'):
                alert.accept()
                registerAllowed = False
            else:
                registerAllowed = True
        except NoAlertPresentException:
            registerAllowed = True

    confirm_present = ec.presence_of_element_located(
        (By.XPATH, "//input[@type='submit' and @value='Confirm to add course(s)']"))
    WebDriverWait(browser, 0).until(confirm_present)
    browser.find_element(By.XPATH, "//input[@type='submit' and @value='Confirm to add course(s)']").click()


schedule.every().day.at('14:00').do(register_course)

"""
if __name__ == "__main__":
    register_course()
"""

while True:
    schedule.run_pending()
    time.sleep(0.2)

