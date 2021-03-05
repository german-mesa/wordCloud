# HANA Exercise
import os
import json

from hdbcli import dbapi

query = """
    SELECT  
        "Title",
        "Requisition ID",
        "Posted Date" as POSTED,
        "Recruiter",
        "Region",
        "Country",
        "City",
        "Work Area" as AREA,
        "Expected Travel",
        "Career Status",
        "Employment Type"
    FROM    
        PUBLICDATA.POSITIONS
"""


def get_connection_options():
    with open(os.path.join(os.getcwd(), 'credentials', 'hana_connection.json')) as json_file:
        return json.load(json_file)


def main():
    # Get environment variables from JSON file
    options = get_connection_options()

    # Construct a Explore Data client object.
    connection = dbapi.connect(
        address=options['address'],
        port=options['port'],
        user=options['user'],
        password=options['password']
    )

    # Preparing cursor
    cursor = connection.cursor()

    # Execute query and count records
    cursor.execute(query)
    positions_df = cursor.fetchall()
    print('{0} records in this table'.format(len(positions_df)))

    # Execute query grouping by some criteria
    query_by_region = "SELECT POSTED, AREA, COUNT(*) " + \
                      "FROM (" + query + ") " + \
                      "GROUP BY POSTED, AREA " + \
                      "ORDER BY POSTED DESC, AREA ASC"

    cursor.execute(query_by_region)
    positions_by_region_df = cursor.fetchall()
    print('{0} records in this table'.format(len(positions_by_region_df)))

    # Close the cursor
    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()
