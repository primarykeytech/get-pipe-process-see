import psycopg2
import config


def copy_from_dynamo():

    # dynamodb copy command example from
    # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/RedshiftforDynamoDB.html
    # copy favoritemovies from 'dynamodb://my-favorite-movies-table'
    # credentials 'aws_access_key_id=<Your-Access-Key-ID>;aws_secret_access_key=<Your-Secret-Access-Key>'
    # readratio 50;

    copy_cmd_str = f"""copy {config.REDSHIFT_TABLE} 
        from 'dynamodb://{config.DB_TABLE}' 
        credentials 'aws_access_key_id={config.ACCESS_KEY};
        aws_secret_access_key={config.SECRET_KEY}'"""

    # conn example from
    # https://stackoverflow.com/questions/45212281/how-to-connect-amazon-redshift-to-python/45213674
    # con=psycopg2.connect("dbname=sales host=redshifttest-xyz.cooqucvshoum.us-west-2.redshift.amazonaws.com port=5439 user=master password=secret")

    # build the connection string.
    conn_string = f"""dbname={config.REDSHIFT_DBNAME} 
        host={config.REDSHIFT_HOST} port={config.REDSHIFT_PORT} 
        user={config.REDSHIFT_USER} password={config.REDSHIFT_PASS}"
        """

    # good syntax tip from
    # https://stackoverflow.com/questions/15601704/copying-data-from-s3-to-aws-redshift-using-python-and-psycopg2
    with psycopg2.connect(conn_string) as conn:
        with conn.cursor() as curs:
            curs.execute(copy_cmd_str)


