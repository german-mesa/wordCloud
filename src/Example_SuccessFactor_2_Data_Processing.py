import os
import csv

from bs4 import BeautifulSoup

URL_ROOT = "https://performancemanager5.successfactors.eu"

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
    'Link'
]


def read_data_extracted_page(file_name):
    # Read file stored into local repository - this needs to be changed to HTTP search in the future
    url_local_file_response = os.path.join(os.getcwd(), "input", file_name)

    print("Scrapping file {0}".format(url_local_file_response))
    file = open(url_local_file_response, "r")
    content = file.read()

    # Response scrapping
    soup = BeautifulSoup(content, features="lxml")

    job_result_list = []

    for table_row in soup.find_all("tr", {"class": "jobResultItem"}):
        # Each table row has a couple of td HTML elements
        cell_detail = table_row.findAll('td')[0]

        job_attributes = cell_detail.findAll("span", {"class": "jobContentEM"})

        job_detail = {
            'Title': cell_detail.find("a", {"class": "jobTitle"}).text,
            'Link': URL_ROOT + cell_detail.find("a", {"class": "jobTitle"}).attrs['href'],
            'Requisition ID': job_attributes[0].text,
            'Posted Date': job_attributes[1].text.replace("Posted on ", ""),
            'Recruiter': job_attributes[2].text,
            'Region': job_attributes[3].text,
            'Country': job_attributes[4].text,
            'City': job_attributes[5].text,
            'Work Area': job_attributes[7].text,
            'Expected Travel': job_attributes[8].text,
            'Career Status': job_attributes[9].text,
            'Employment Type': job_attributes[10].text
        }

        job_result_list.append(job_detail)

    print("End of scrapping {0}".format(url_local_file_response))

    return job_result_list


def compose_final_report(search_result):
    if not search_result:
        print("Search result is empty")

    url_local_file_report = os.path.join(os.getcwd(), "datasets", "open_positions.csv")

    print("Composing final export")
    try:
        with open(url_local_file_report, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=';')
            writer.writeheader()

            for data in search_result:
                writer.writerow(data)

            csvfile.close()

    except IOError:
        print("I/O error")

    print("End of the export process")


def main():
    search_result = []

    # Read all the files into the input directory
    for file in os.listdir(os.path.join(os.getcwd(), "input")):
        if file.endswith(".html"):
            search_result.extend(read_data_extracted_page(file))

    # Create report using open positions
    compose_final_report(search_result)


if __name__ == '__main__':
    main()
