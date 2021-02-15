# https://pypi.org/project/selenium/
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

search_question = "SAP"


def main():
    driver = webdriver.Chrome()

    # Open Google in Chrome
    driver.get('http://www.google.com')
    assert 'Google' in driver.title

    # Active the iframe and click the agree button
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe")))
    agree = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="introAgreeButton"]/span/span')))
    agree.click()

    # Back to the main page and search a basic text
    driver.switch_to.default_content()

    search = driver.find_element_by_class_name("gLFyf")
    search.send_keys(search_question)
    search.send_keys(Keys.ENTER)
    time.sleep(3)


if __name__ == '__main__':
    main()
