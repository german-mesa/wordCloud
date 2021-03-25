# https://www.scrapingbee.com/blog/selenium-python/
#
import os

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DRIVER_PATH = os.path.join(os.getcwd(), 'drivers', 'chromedriver')

url_service_catalogue = 'https://servicescatalog.cvdp3eof-dbsservic1-p1-public.model-t.cc.commerce.ondemand.com'


def read_service_dataset():
    # Variables to locate the initial dataset
    excel_file_path = os.path.join(os.getcwd(), 'datasets', 'I4N Services 2021.xlsx')
    excel_sheet_name = 'I4N Services Mar\'21'

    # Read services from file
    services = pd.read_excel(excel_file_path, header=0, sheet_name=excel_sheet_name)

    # Adding extra columns
    services['Actual Release Date'] = ""
    services['Status'] = ""
    services['Version'] = ""
    services['Version Date'] = ""

    services['Engagement Type'] = ""
    services['Portfolio area'] = ""
    services['Service category'] = ""
    services['Service type'] = ""
    services['Line of service'] = ""
    services['Industry'] = ""

    services['Service One Page'] = ""
    services['Service One Page Link'] = ""

    services['Service Offering Manager'] = ""
    services['Portfolio Area Manager'] = ""
    services['Global Service Owner'] = ""

    return services


def services_catalogue_extraction(dataset):
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    for index, row in dataset.iterrows():
        try:
            # Connect to Service & Support catalogue
            driver.get(url_service_catalogue)

            # Introduce the service number
            inputElement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "js-site-search-input"))
            )
            inputElement.click()
            inputElement.send_keys(row['CRM#'])

            # Search service number and navigate to the detail
            inputElement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".name"))
            )
            inputElement.click()

            # Let's scrap all the data in the page
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')

            # Service name
            dataset.at[index, 'OneVoice Service Name'] = soup.find_all('div', class_='product-details')[0].text

            # Header details
            header_details = soup.find_all('dl', class_='sc-pdp-header-details__list')[0]
            for item in list(zip(header_details.find_all("dt"), header_details.find_all("dd"))):
                category, value = item

                if "Version:" == category.text:
                    dataset.at[index, 'Version'] = value.text

                if "Version date:" == category.text:
                    dataset.at[index, 'Version Date'] = value.text

                if "Status:" == category.text:
                    dataset.at[index, 'Status'] = value.text

            # Contact Details
            contacts = soup.find_all('li', class_='sc-contact')
            for item in contacts:
                role = item.find_all('p', 'sc-contact--role')
                name = item.find('a').text

                if "Offering" in role[0].text:
                    dataset.at[index, 'Service Offering Manager'] = name

                if "Portfolio" in role[0].text:
                    dataset.at[index, 'Portfolio Area Manager'] = name

                if "Global" in role[0].text:
                    dataset.at[index, 'Global Service Owner'] = name

            # Tab container
            container = soup.find('div', 'tab-container')

            # Document extraction
            documents = container.find(id='table-sortable')
            if documents is not None:
                documents = documents.find_all('a')
                for document in documents:
                    if 'Service One Page' in document.text:
                        dataset.at[index, 'Service One Page'] = document.text
                        dataset.at[index, 'Service One Page Link'] = document.get('href')

            # Properties extraction
            properties = container.find_all('table', class_='table table-condensed sc-table')
            properties = properties[0].find('tbody')
            for item in properties.find_all('tr'):
                category = item.find('td', 'attrib')
                value = item.find_all('td')[1].text

                if "Actual Release Date" in category.text:
                    dataset.at[index, 'Actual Release Date'] = value

                if "Engagement Type" in category.text:
                    dataset.at[index, 'Engagement Type'] = value

                if "Portfolio area" in category.text:
                    dataset.at[index, 'Portfolio area'] = value

                if "Service category" in category.text:
                    dataset.at[index, 'Service category'] = value

                if "Service type" in category.text:
                    dataset.at[index, 'Service type'] = value

                if "Line of service" in category.text:
                    dataset.at[index, 'Line of service'] = value

                if "Industry" in category.text:
                    dataset.at[index, 'Industry'] = value

        except WebDriverException:
            print('Could not open the Service Catalogue')


def compose_final_report(dataset):
    if dataset.empty:
        print("Dataset is empty")

    url_local_file_report = os.path.join(os.getcwd(), "datasets", "services.xlsx")

    try:
        dataset.to_excel(url_local_file_report, sheet_name='Scrapped Services')

    except IOError:
        print("I/O error")


def main():
    # Read services dataset
    services = read_service_dataset()

    # Get details from Service & Support Catalogue
    services_catalogue_extraction(services)

    # Export to Excel
    compose_final_report(services)


if __name__ == '__main__':
    main()
