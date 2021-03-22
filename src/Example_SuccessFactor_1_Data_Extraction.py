# https://www.scrapingbee.com/blog/selenium-python/
#
import io
import os
import time
import datetime

from os import listdir
from os.path import isfile, join

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH = os.path.join(os.getcwd(), 'drivers', 'chromedriver')

url_navigation_list = [
    # SSO at SAP
    'https://accounts.sap.com/saml2/idp/usso/sap?sp=www.successfactors.com',
    # Success Factors - Find internal Jobs
    'https://performancemanager5.successfactors.eu/sf/careers/jobsearch?bplte_company=SAP',
    # Success Factors - Search positions button
    'https://performancemanager5.successfactors.eu/acme?bplte_company=SAP&fbacme_n=recruiting&recruiting%5fns=joblisting%20summary&itrModule=rcm',
]


def chrome_head_full_mode():
    page_counter = 0

    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    for url in url_navigation_list:
        driver.get(url)

    time.sleep(10)

    try:
        # Select number of records per page
        select = Select(driver.find_element_by_xpath("//select[@id='37:']"))
        select.select_by_visible_text("150")
        time.sleep(2)

        while True:
            # Endless loop until next button is disabled
            element = driver.find_elements_by_id("36:_next")
            if len(element) < 2:
                break

            # Export page for later use
            page_counter = page_counter + 1
            export_page_source(driver.page_source, page_counter)
            time.sleep(15)

            # Click on next button
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, '36:_next'))).click()
            time.sleep(15)

    except NoSuchElementException:
        print('Could not find the element')

    print("Done")


def get_file_name(page_counter):
    current_day = datetime.date.today()
    year, week_num, day_of_week = current_day.isocalendar()

    return os.path.join(os.getcwd(), 'output',
                        'response-{week}-{counter}.html'.format(week=str(week_num), counter=page_counter))


def export_page_source(page_source, page_counter):
    page_name = get_file_name(page_counter)

    try:
        with io.open(page_name, 'w') as file:
            file.write(page_source)

    except IOError:
        print("I/O error")


def move_output_files():
    print("Moving files to input directory...")

    source_dir = os.path.join(os.getcwd(), 'output')
    destination_dir = os.path.join(os.getcwd(), 'input')

    for file in [f for f in listdir(source_dir) if isfile(join(source_dir, f))]:
        source_file = os.path.join(source_dir, file)
        destination_file = os.path.join(destination_dir, file)

        print(f"Moving...{source_file} to {destination_file}")
        os.rename(source_file, destination_file)


def main():
    # Run chrome at head full mode
    chrome_head_full_mode()

    # Moving files to directory for next step in the process
    move_output_files()


if __name__ == '__main__':
    main()
