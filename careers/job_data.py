import requests
import config
import json
import boto3


def send_to_dynamo(json_data):

    # test that we received data from api_call
    #for row in json_data['jobs']:
    #    print(row['title'])

    # columns that will be needed
    # id (uuid), title, location, snippet (strip html), salary, source,
    # type, link, company, updated

    # sample code from amazon
    # if not dynamodb:
    #     dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    #
    # table = dynamodb.Table('Movies')
    # response = table.put_item(
    #    Item={
    #         'year': year,
    #         'title': title,
    #         'info': {
    #             'plot': plot,
    #             'rating': rating
    #         }
    #     }
    # )
    # return response


    return True


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
