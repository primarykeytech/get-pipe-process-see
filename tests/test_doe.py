import config
import requests
import csv
import os


def test_api_conn():
    """
    Simply testing to see if we can run a request on
    the api. Looking for status code 200.
    """
    qry_string = config.doe_api + \
                 'schools.json?api_key=' + config.doe_key + \
                 '&per_page=5' \
                 '&page=0' + \
                 '&school.region_id=' + str(0) + \
                 '&fields=metadata'

    # get the first page of data from the api.
    response = requests.request('GET', qry_string)

    # only checking if we were successfully able to connect.
    assert response.status_code == 200


def test_read_write_csv():
    """
    Tests whether a csv file can be created to the output
    directory, have data added to it, and then deleted.
    """
    # set the location and name of the csv file.
    output_file = 'output/test_doe.csv'

    # test writing csv file.
    with open(output_file, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    # boolean for the test.
    read_correctly = False

    # list for the results of reading csv.
    results = []

    # read from csv file.
    with open(output_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            results.append(row)
        # get just the first value.
        single_value = results[0][0]

        # determine if the first value is spam.
        read_correctly = single_value == 'Spam'

    # delete the file.
    os.remove(output_file)

    # run the test.
    assert True if read_correctly else False
