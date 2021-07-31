import requests
import config
import json
import csv


def __build_get_string(api_location, api_key, page_no,
                       per_page, region):

    # build the querystring based on doe documentation.
    qry_string = config.doe_api + \
                 'schools.json?api_key=' + config.doe_key + \
                 '&per_page=' + str(per_page) + \
                 '&page=' + str(page_no) + \
                 '&school.region_id=' + str(region) + \
                 '&fields=id,school,latest'
    return qry_string


def __build_meta_string(api_location, api_key, region):
    # build the querystring based on doe documentation.
    qry_string = config.doe_api + \
                 'schools.json?api_key=' + config.doe_key + \
                 '&per_page=10' \
                 '&page=0' + \
                 '&school.region_id=' + str(region) + \
                 '&fields=metadata'
    return qry_string

# def __handle_requests(qry_string):

def __gen_meta_dict(per_page):

    # dictionary to return.
    dict_return = {}

    # we will be iterating through each DOE region from 0-9
    # and starting with page 0 so that we can get the total
    # number of records from the metadata.
    for region in range(10):

        # build the query string.
        qry_string = __build_meta_string(config.doe_api,
                                         config.doe_key, region)

        # # build the query string.
        # qry_string = __build_get_string(config.doe_api,
        #                                 config.doe_key, 0,
        #                                 per_page, region)

        # get the first page of data from the api.
        response = requests.request('GET', qry_string)

        # get the status to decide if we should continue.
        if response.status_code != 200:
            print("Error retrieving data from DOE API.")
            return

        # get the json out of the response.
        json_data = response.json()

        # get the total number of records from the metadata.
        meta = json_data['metadata']
        total_region = meta['total']
        print(f"Region {region} records: {total_region}")

        dict_return[region] = total_region

        # calculate pages based on records per request and total.
        pages = (int(total_region) // per_page) + 1
        print(f'Region {region} pages: {pages}')

    return dict_return

def get_api_data():

    # we will be returning the total number of records.
    total_records = 0

    # set how many records we want per page. 100 is the max.
    per_page = 100

    # get a dictionary with the
    meta_dict = __gen_meta_dict(per_page)


        #total_records += total_region

        #print(total_records)
    return total_records

    # # figure out paging.
    #
    # # saving the json to a file so we can look at it if necessary.
    # with open('doe_json.txt', 'w') as outfile:
    #     json.dump(response.json(), outfile)
    #
    # # get just the results minus the metadata.
    # json_results = json_data['results']
    #
    # # now we will open a file for writing
    # data_file = open('doe.csv', 'w')
    #
    # # create the csv writer object
    # csv_writer = csv.writer(data_file, lineterminator='\n',
    #                         quoting=csv.QUOTE_NONNUMERIC)
    #
    # # Counter variable used for writing
    # # headers to the CSV file
    # count = 0
    #
    # # iterate through results.
    # for result in json_results:
    #     if count == 0:
    #         # Writing headers of CSV file
    #         header = result.keys()
    #         csv_writer.writerow(header)
    #         count += 1
    #
    #     # Writing data of CSV file
    #     csv_writer.writerow(result.values())
    #
    # # close out.
    # data_file.close()
    #
    # # return the results in json format.
    # return json_results

