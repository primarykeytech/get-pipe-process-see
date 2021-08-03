import requests
import config
import csv


def api_call(the_job, location):

    # total jobs will be returned.
    total_jobs = 0

    # build the url with values from the config file.
    url = config.career_api + config.career_key

    # add a header since it is in the one and only example we
    # are given from the provider.
    header = {'Content-type': 'application/json'}

    # there is no documentation but the one example includes
    # keywords and location fields.
    body = "{'keywords': '" + the_job + "', 'location': '" + location + "'}"

    # post the request and get the response.
    response = requests.post(url, data=body, headers=header)

    # make sure we have a success.
    if response.status_code != 200:
        # exit out of function
        return total_jobs

    # output json to text to save in case of errors.

    # get the total jobs for the call.

    # save results to dynamodb.



    print(response.status_code)
    print(response.json())

