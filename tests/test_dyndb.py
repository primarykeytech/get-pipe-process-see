from dba.dynamodb import dyn_crud


def test_create_dyn():
    """
    Tests the creation of a record in dynamodb.
    :return:
    """
    # create an id.
    # the_id = str(uuid.uuid1())
    the_id = 'from-test-dyndb'

    # create a row of data
    row = {'id': the_id, 'company': 'test company',
           'title': 'CEO', 'type': '1',
           'location': 'Shambhala', 'snippet': 'This is a test.',
           'salary': '$100', 'source': 'LinkedIn',
           'the_type': 'Some type', 'link': 'my link',
           'updated': '2021-01-01 00:00:00'}

    # create the record and get the bool.
    success = dyn_crud.create_record(row)

    # run the test.
    assert True if success else False


def test_retrieve_dyn():
    """
    Retrieves the test record from dynamodb.
    """
    # use the same id as previous test.
    the_id = 'from-test-dyndb'

    # get the response using the
    response = dyn_crud.retrieve_record(the_id)

    # run test.
    assert True if (response['company']['S'] == 'test company' and
                    response['location']['S'] == 'Shambhala') else False


def test_delete_dyn():
    """
    Deletes the test record from dynamodb.
    :return:
    """
    # use the same id as previous test.
    the_id = 'from-test-dyndb'

    # create the record and get the bool.
    success = dyn_crud.delete_record(the_id)

    # run the test.
    assert True if success else False
