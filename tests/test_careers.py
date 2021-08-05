import config
import requests


def test_job_api():

    # build the url with values from the config file.
    url = config.career_api + config.career_key

    # add a header.
    header = {'Content-type': 'application/json'}

    # build the payload.
    body = "{'keywords': 'casino', 'location': 'Reno,NV'}"

    # post the request and get the response.
    response = requests.post(url, data=body, headers=header)

    # only checking if we were successfully able to connect.
    assert response.status_code == 200
