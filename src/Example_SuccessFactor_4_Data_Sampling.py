# HANA Exercise
import json
import os

import pandas as pd
from hana_ml.dataframe import ConnectionContext, DataFrame, create_dataframe_from_pandas

query = """
    SELECT  
        'Title',
        'Requisition ID',
        'Posted Date' as DATE,
        'Recruiter',
        'Region',
        'Country',
        'City',
        'Work Area' as AREA,
        'Expected Travel',
        'Career Status',
        'Employment Type'
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
    with ConnectionContext(options['address'], options['port'], options['user'], options['password']) as connection:
        # Execute query and count records
        positions_df = connection.sql(query)
        print('{0} records in this table'.format(positions_df.count()))

        # Execute query grouping by some criteria
        query_by_region = "SELECT DATE, AREA, COUNT(*) FROM (" + query + ") GROUP BY DATE, AREA"
        positions_by_region_df = connection.sql(query_by_region)
        print('{0} records in this table'.format(positions_by_region_df.count()))


if __name__ == '__main__':
    main()
