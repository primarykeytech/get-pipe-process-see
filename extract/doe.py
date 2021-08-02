import requests
import config
import csv


def __build_get_string(api_location, api_key, page_no,
                       per_page, region):
    """
    Creates the querystring for the api get request.
    Created: 2021-08-01 by PKT-JW.
    :param api_location: DOE college scorecard api location.
    :param api_key: The assigned api key.
    :param page_no: The API requires paging for large results.
    :param per_page: Records to request per page. Documentation states that
    maximum is 100.
    :param region: College region. Documentation shows 0-9.
    :return: The querystring used to make the request.
    """
    # build the querystring based on doe documentation.
    qry_string = config.doe_api + \
                 'schools.json?api_key=' + config.doe_key + \
                 '&per_page=' + str(per_page) + \
                 '&page=' + str(page_no) + \
                 '&school.region_id=' + str(region) + \
                 '&fields=id,school,latest'
    return qry_string


def __build_meta_string(api_location, api_key, region):
    """
    Builds the minimal request to send to the api that should
    only result in the meta data. This will allows us to obtain
    the total result per region.
    Created: 2021-08-01 by PKT-JW.
    :param api_location: DOE college scorecard api location.
    :param api_key: The assigned api key.
    :param region: College region. Documentation shows 0-9.
    :return: The querystring used to make the request.
    """

    # build the querystring based on doe documentation.
    qry_string = config.doe_api + \
                 'schools.json?api_key=' + config.doe_key + \
                 '&per_page=10' \
                 '&page=0' + \
                 '&school.region_id=' + str(region) + \
                 '&fields=metadata'
    return qry_string


def __handle_requests(per_page, meta_dict, output_file):
    """
    The function that is used to make the actual requests
    against the api. Receives the responses and appends to
    the csv file set as the argument.
    Created: 2021-08-01 by PKT-JW.
    :param per_page: Records to request per page. Documentation states that
    maximum is 100.
    :param meta_dict: dictionary of pages needed per region.
    :param output_file: location and name of output csv file.
    :return: Boolean indicating if process is a success.
    """

    # iterate through dictionary. we are assuming that the
    # number of regions is 0-9 based on the documentation.
    for region in range(10):

        # get the record count from the dict.
        total_region = meta_dict[region]

        # calculate pages based on records per request and total.
        pages = (int(total_region) // per_page) + 1
        print(f'Region {region} pages: {pages}')

        # iterate through pages and make individual requests.
        for page in range(pages):
            print(f'Getting Region {region} - Page {page}')

            # build the query string.
            qry_string = __build_get_string(config.doe_api,
                                            config.doe_key, page,
                                            per_page, region)

            # get the first page of data from the api.
            response = requests.request('GET', qry_string)

            # get the status to decide if we should continue.
            if response.status_code != 200:
                print("Error retrieving data from DOE API.")
                return

            # get the json out of the response.
            json_data = response.json()

            # get just the results minus the metadata.
            json_results = json_data['results']

            # now we will open a file for appending but will
            # create the file if it does not exist.
            data_file = open(output_file, 'a+')

            # create the csv writer object
            csv_writer = csv.writer(data_file, lineterminator='\n',
                                    quoting=csv.QUOTE_NONNUMERIC)

            # Counter variable used for writing
            # headers to the CSV file
            count = 0

            # iterate through results.
            for result in json_results:
                if region == 0 and page == 0 and count == 0:
                    # Writing headers of CSV file
                    header = result.keys()
                    csv_writer.writerow(header)
                    count += 1

                # Writing data of CSV file
                csv_writer.writerow(result.values())

            # close out.
            data_file.close()

    # return success.
    return True


def __gen_meta_dict():
    """
    Creates a dictionary that gets the total number of records
    for each of the regions. Makes a minimal request against the
    api and then gets the meta data values to achieve this goal.
    Created: 2021-08-01 by PKT-JW.
    :return: dictionary where key is region and value is total count.
    """

    # dictionary to return.
    dict_return = {}

    # we will be iterating through each DOE region from 0-9
    # and starting with page 0 so that we can get the total
    # number of records from the metadata.
    for region in range(10):

        # build the query string.
        qry_string = __build_meta_string(config.doe_api,
                                         config.doe_key, region)

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

        # set the dictionary value.
        dict_return[region] = total_region

    return dict_return


def get_api_data():
    """
    Runs the operation to get the data from the api. First makes
    a minimal request for each region to get the total number of
    records. Uses info to determine number of pages per region. Then,
    makes the full requests for each region by page. Saves all info in
    a csv file.
    Created: 2021-08-01 by PKT-JW.
    :return: total records retrieved.
    """

    # we will be returning the total number of records.
    total_records = 0

    # set how many records we want per page. 100 is the max.
    per_page = 100

    # set the location and name of the csv file.
    output_file = 'output/doe.csv'

    # get a dictionary with the counts of records per region.
    meta_dict = __gen_meta_dict(per_page)

    # set the total records as we will be returning this value.
    total_records = sum(meta_dict.values())
    print(f'Total records:{total_records}')

    # send dictionary to function to build csv with multiple
    # requests to api.
    if __handle_requests(per_page, meta_dict, output_file):
        print('CSV file created.')

    # send back just the total count.
    return total_records

