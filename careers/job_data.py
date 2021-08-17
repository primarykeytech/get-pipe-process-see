import requests
import config
import json
from dba.dynamodb import dyn_crud


def __build_job_api(api_location, api_key, the_job, location, page_no):
    """
    Creates the querystring for the api get request from jooble.
    Created: 2021-08-09 by PKT-JW.
    :param api_location: jooble api location.
    :param api_key: The assigned api key.
    :param page_no: The API page.
    :param per_page: Records to request per page. Experimenting shows only 20 max.
    :return: The querystring used to make the request.
    """
    # build the querystring based on doe documentation.
    url = api_location + api_key

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
           "', 'page': " + str(page_no) + "}"

    # return a tuple with the info.
    return url, header, body


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


def __handle_requests(per_page, total_jobs, the_job, location):

    # total jobs added to dynamo will be returned.
    total_added = 0

    # create the file name for results.
    the_file = 'output/' + location + '-' + the_job + '.json'

    # calculate pages based on records per request and total.
    pages = (int(total_jobs) // per_page) + 1
    print(f'{the_job} - {location}: {pages} pages...')

    # iterate through pages and make individual requests.
    for page in range(pages):
        print(f'{the_job} - {location} - Page {page}')

        # get the elements needed for api call.
        url, header, body = __build_job_api(config.career_api, config.career_key,
                                            the_job, location, page)

        # build the query string.
        response = requests.post(url, data=body, headers=header)

        # make sure we have a success.
        if response.status_code != 200:
            # exit out of function
            return total_jobs

        # output json to text to save in case of errors.
        with open(the_file, 'a+') as f:
            json.dump(response.json(), f)

        # get a count of how many to add.
        data = response.json()
        total_added += len(data['jobs'])

        # send json to function to save results to dynamodb.
        # will return True if successful.
        sent_to_dynamo = send_to_dynamo(data)

        # check bool to make sure succeeded.
        if not sent_to_dynamo:
            return 0

    # return the total number of jobs added to dynamo,
    return total_added


def api_call(the_job, location):
    """
    Handles the calls to the api based on the job selected
    and the location set.
    :param the_job: job title e.g. programmer
    :param location: city and state e.g. Portland, OR
    :return: total number of jobs that meet criteria.
    """

    # total added to dynamo will be returned.
    total_added = 0

    # we appear to be limited to 20 records per page.
    per_page = 20

    # create an initial request to get the total number.
    url, header, body = __build_job_api(config.career_api, config.career_key,
                                        the_job, location, 1)

    # post the request and get the response.
    response = requests.post(url, data=body, headers=header)

    # make sure we have a success.
    if response.status_code != 200:
        # exit out of function
        return total_added

    # get the data from the response.
    data = response.json()

    # get the total jobs for the call to return.
    total_jobs = int(data["totalCount"])

    # send the total count to the function that will handle paging.
    # get the total number added to dynamo.
    total_added = __handle_requests(per_page, total_jobs, the_job, location)

    # return the number of jobs added.
    return total_added
