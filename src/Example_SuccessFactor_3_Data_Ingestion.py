# HANA Exercise
import json
import os

import pandas as pd
from hana_ml.dataframe import ConnectionContext, create_dataframe_from_pandas

query = """
    SELECT  
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
        'Employment Type'
    FROM    
        PUBLICDATA.POSITIONS
"""

CSV_COLUMNS = [
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
    'Employment Type'
]


def get_connection_options():
    with open(os.path.join(os.getcwd(), 'credentials', 'hana_connection.json')) as json_file:
        return json.load(json_file)


def main():
    # Get environment variables from JSON file
    options = get_connection_options()

    # Construct a Explore Data client object.
    with ConnectionContext(options['address'], options['port'], options['user'], options['password']) as connection:
        # Create SAP HANA Cloud table from pandas dataframe
        positions_df = pd.read_csv(
            filepath_or_buffer=os.path.join(os.getcwd(), 'datasets', 'open_positions.csv'),
            sep=';',
            parse_dates=True
        )

        positions_df = create_dataframe_from_pandas(connection_context=connection,
                                                    pandas_df=positions_df,
                                                    table_name='POSITIONS',
                                                    schema='PUBLICDATA',
                                                    force=True,
                                                    replace=True)

        print(positions_df.select_statement)

        # Execute query and count records
        positions_df = connection.sql(query)
        print('{0} records in this table'.format(positions_df.count()))


if __name__ == '__main__':
    main()
