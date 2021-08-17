import boto3
import config
import re
import uuid


def create_record(row):
    """
    Creates a new record in the dynamodb database table.
    :param row: json row with data to be added.
    :return: True if success.
    """

    # create the boto3 object.
    dynamodb = boto3.resource('dynamodb',
                              region_name=config.AWS_REGION)

    # set the table from the cfg file.
    table = dynamodb.Table(config.DB_TABLE)

    # create a new id since we can't necessarily trust the one
    # coming from the api.
    if row['id'] == 'from-test-dyndb':
        the_id = 'from-test-dyndb'
    else:
        the_id = str(uuid.uuid1())

    # the field snippet appears to have a lot of html so let us
    # strip out the tags before saving.
    the_desc = re.sub('<[^<]+?>', '', row['snippet'])

    # add the item.
    response = table.put_item(
        Item={
            # create an id rather than using ones from result.
            'id': the_id,
            'title': row['title'] if row['title'] is not None else '',
            'company': row['company'] if row['company'] is not None else '',
            'location': row['location'] if row['location'] is not None else '',
            'snippit': the_desc,
            'salary': row['salary'] if row['salary'] is not None else '',
            'source': row['source'] if row['source'] is not None else '',
            'the_type': row['type'] if row['type'] is not None else '',
            'the_link': row['link'] if row['link'] is not None else '',
            'updated': row['updated'] if row['updated'] is not None else ''
        }
    )

    # make sure it succeeded.
    the_status = response['ResponseMetadata']['HTTPStatusCode']
    bool_rtn = True if the_status == 200 else False

    # return success here.
    return bool_rtn


def retrieve_record(record_id):

    # create the boto3 object.
    client = boto3.client('dynamodb', region_name=config.AWS_REGION)

    # set the table from the cfg file.
    # table = dynamodb.Table(config.DB_TABLE)

    # get the record by id.
    response = client.get_item(
        TableName=config.DB_TABLE, Key={'id': {'S': record_id}}
    )

    # get just the items.
    item = response['Item']
    return item


def retrieve_record_by_location_title(location, title):

    # create the boto3 object.
    # dynamodb = boto3.resource('dynamodb',
    #                           region_name=config.AWS_REGION)
    client = boto3.client('dynamodb', region_name=config.AWS_REGION)

    # set the table from the cfg file.
    # table = dynamodb.Table(config.DB_TABLE)

    # get the record by id.
    response = client.get_item(
        TableName=config.DB_TABLE,
        Key={'location': {'S': location}, 'title': {'S': title}}
    )

    item = response['Item']
    return item


def list_records(title, location):
    pass


def delete_record(record_id):

    # create the boto3 object.
    dynamodb = boto3.resource('dynamodb',
                              region_name=config.AWS_REGION)

    # set the table from the cfg file.
    table = dynamodb.Table(config.DB_TABLE)

    # perform the operation.
    response = table.delete_item(Key={'id': record_id})

    # make sure it succeeded.
    the_status = response['ResponseMetadata']['HTTPStatusCode']
    bool_rtn = True if the_status == 200 else False

    # return success here.
    return bool_rtn
