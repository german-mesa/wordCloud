# https://www.scrapingbee.com/blog/selenium-python/
#
import csv
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

WAIT_TIME = 15
ITEMS_PER_PAGE = "150"
DRIVER_PATH = os.path.join(os.getcwd(), 'drivers', 'chromedriver')

url_navigation_list = [
    # SSO at SAP
    'https://accounts.sap.com/saml2/idp/usso/sap?sp=www.successfactors.com',
    # Success Factors - Find internal Jobs
    'https://performancemanager5.successfactors.eu/sf/careers/jobalerts?bplte_company=SAP&_s.crb=ItBw0C1Sv0IrR%252b%252f21V6%252fJ16NDz3tkTjE4K7kVsR0hBk%253d'
]

csv_columns = [
    'Title',
    'Requisition ID',
    'Posted Date',
    'Recruiter',
    'Region',
    'Country',
    'City',
    'Work Area',
    'Expected Travel',
    'Career Status',
    'Employment Type',
    'Hiring Manager',
    'Manager',
    'Job Title',
    'Career Level',
    'Grade Level'
]


def scraping_open_positions():
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.maximize_window()

    for url in url_navigation_list:
        driver.get(url)

    try:
        # Execute saved search - only have one
        driver.find_element_by_css_selector(css_selector='.floatright').click()
        driver.find_element_by_id('runJobAlert_alertRow131243980').click()

        # Page size set to 150 elements
        select = Select(
            WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.ID, "37:")))
        )
        select.select_by_visible_text(ITEMS_PER_PAGE)
        time.sleep(5)

        # Initializing the counter
        job_count = 0

        # Let's scrap all the data in the page
        while True:
            # Endless loop until next button is disabled
            element = driver.find_elements_by_id("36:_next")
            if len(element) < 2:
                break

            # Extract data from page for later use
            job_result_list = scrap_job_list_from_page(driver.page_source)

            # Loop through all the opportunities and get content
            for job_result_item in job_result_list:
                # Scrapping job
                job_count = job_count + 1
                print(f"Scrapping job {job_count}...{job_result_item['Title']}")

                # Navigate to the position
                element = WebDriverWait(driver, WAIT_TIME).until(
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, job_result_item['Title']))
                )
                element.click()

                # Extract job details from the position
                scrap_job_details_from_page(job_result_item, driver.page_source)

                # Return to the job list
                element = driver.find_element_by_css_selector(".globalFloatRight:nth-child(1) > "
                                                              ".globalSecondaryButton:nth-child(1)")
                element.click()

                # Wait sometime for page to be reloaded
                time.sleep(WAIT_TIME)

            # Compose final export
            compose_final_report(job_result_list)

            # Click on next button
            element = WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.ID, "36:_next")))
            element.click()

            # Wait sometime for page to be reloaded
            time.sleep(WAIT_TIME)

    except NoSuchElementException:
        print('Could not find the element')

    finally:
        driver.close()


def scrap_job_list_from_page(page_source):
    soup = BeautifulSoup(page_source, features="lxml")
    job_result_list = []

    for table_row in soup.find_all("tr", {"class": "jobResultItem"}):
        # Each table row has a couple of td HTML elements
        cell_detail = table_row.findAll('td')[0]

        job_attributes = cell_detail.findAll("span", {"class": "jobContentEM"})

        job_detail = {
            'Title': cell_detail.find("a", {"class": "jobTitle"}).text,
            'Requisition ID': job_attributes[0].text,
            'Posted Date': job_attributes[1].text.replace("Posted on ", ""),
            'Recruiter': job_attributes[2].text,
            'Region': job_attributes[3].text,
            'Country': job_attributes[4].text,
            'City': job_attributes[5].text,
            'Work Area': job_attributes[7].text,
            'Expected Travel': job_attributes[8].text,
            'Career Status': job_attributes[9].text,
            'Employment Type': job_attributes[10].text,
            'Hiring Manager': '',
            'Manager': '',
            'Job Title': '',
            'Career Level': '',
            'Grade Level': ''
        }

        job_result_list.append(job_detail)

    return job_result_list


def scrap_job_details_from_page(job_result_item, page_source):
    soup = BeautifulSoup(page_source, features="lxml")

    for field in soup.select('.headerContent > p > span'):
        for text in str.splitlines(field.text):
            text = text.replace("&nbsp", "")

            if 'Hiring Manager:' in text:
                job_result_item['Hiring Manager'] = text.split(':')[1]

            if 'Manager:' in text:
                job_result_item['Manager'] = text.split(':')[1]

            if 'Job Title:' in text:
                job_result_item['Job Title'] = text.split(':')[1]

            if 'Career Level:' in text:
                job_result_item['Career Level'] = text.split(':')[1]

            if 'Grade Level:' in text:
                job_result_item['Grade Level'] = text.split(':')[1]


def compose_final_report(search_result):
    if not search_result:
        print("Search result is empty")

    url_local_file_report = os.path.join(os.getcwd(), "datasets", "open_positions.csv")

    try:
        with open(url_local_file_report, 'a+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=';')
            writer.writeheader()

            for data in search_result:
                writer.writerow(data)

            csvfile.close()

    except IOError:
        print("I/O error")


def main():
    # Open SuccessFactor and scrape open positions
    scraping_open_positions()


if __name__ == '__main__':
    main()
