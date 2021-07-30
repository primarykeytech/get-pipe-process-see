import requests
import config
import json
import csv


def get_api_data():
    # build the query string.
    # qry_string = 'https://api.data.gov/ed/collegescorecard/v1/' \
    #     'schools?api_key=' + config.doe_key

    qry_string = 'https://api.data.gov/ed/collegescorecard/v1/' \
            'schools.json?api_key=' + config.doe_key + \
            '&per_page=100' \
            '&school.region_id=6' \
            '&fields=id,school,latest'

    # get the data from the api.
    response = requests.request('GET', qry_string)

    # get the status to decide if we should continue.

    # get the json out of the response.
    json_data = response.json()

    # get the total number of records.

    # figure out paging.

    # saving the json to a file so we can look at it if necessary.
    with open('doe_json.txt', 'w') as outfile:
        json.dump(response.json(), outfile)

    # get just the results minus the metadata.
    json_results = json_data['results']

    # now we will open a file for writing
    data_file = open('doe.csv', 'w')

    # create the csv writer object
    csv_writer = csv.writer(data_file, lineterminator='\n',
                            quoting=csv.QUOTE_NONNUMERIC)

    # Counter variable used for writing
    # headers to the CSV file
    count = 0

    # iterate through results.
    for result in json_results:
        if count == 0:
            # Writing headers of CSV file
            header = result.keys()
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_writer.writerow(result.values())

    # close out.
    data_file.close()

    # return the results in json format.
    return json_results
