import requests
import config
import json
from dba.dynamodb import dyn_crud


def send_to_dynamo(json_data):
    """
    Writes the records in the json_data object and sends
    it to the DynamoDB instance set in the config.py file.
    :param json_data: data from the api as json.
    :return: True if success.
    """

    # iterate through the jobs.
    for row in json_data['jobs']:

        # send to the data layer.
        success = dyn_crud.create_record(row)

    # return success here.
    return True


def api_call(the_job, location):
    """
    Handles the calls to the api based on the job selected
    and the location set.
    :param the_job: job title e.g. programmer
    :param location: city and state e.g. Portland, OR
    :return: total number of jobs that meet criteria.
    """

    # total jobs will be returned.
    total_jobs = 0

    # build the url with values from the config file.
    url = config.career_api + config.career_key

    # add a header since it is in the one and only example we
    # are given from the provider.
    header = {'Content-type': 'application/json'}

    """
    Appears that api only returns 20 records at a time and without 
    documentation, I can't find how to change the setting. By 
    experimenting and exploring how the api is used on the live 
    jooble site, I found that I could set a page variable. 
    TODO: Handle the paging to retrieve all records for the 
    location and keyword.
    """

    # there is no documentation but the one example includes
    # keywords and location fields.
    # body = "{'keywords': '" + the_job + "', 'location': '" + location + "'}"
    body = "{'keywords': '" + the_job + \
           "', 'location': '" + location + \
           "', 'page': 2}"

    # post the request and get the response.
    response = requests.post(url, data=body, headers=header)

    # make sure we have a success.
    if response.status_code != 200:
        # exit out of function
        return total_jobs

    # get the data from the response.
    data = response.json()

    # get the total jobs for the call to return.
    total_jobs = int(data["totalCount"])

    # create the file name for results.
    the_file = 'output/' + location + '-' + the_job + '.json'

    # output json to text to save in case of errors.
    with open(the_file, 'a+') as f:
        json.dump(response.json(), f)

    # send json to function to save results to dynamodb.
    # will return True if successful.
    sent_to_dynamo = send_to_dynamo(data)

    # check bool to make sure succeeded.
    if not sent_to_dynamo:
        return 0

    # return the number of jobs retrieved.
    return total_jobs
