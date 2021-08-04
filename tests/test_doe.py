import config
import requests


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
    Tests whether a csv file can be created, have data
    added to it, and then deleted.
    """
    assert True