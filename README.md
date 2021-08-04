# get-pipe-process-see
This demo project in Python will provide examples of 
connecting to multiple API's, storing the data in 
multiple places, piping the data to a warehouse, 
processing with Apache Spark, and then visualizing the 
processed data. 

Obviously, this would not be the actual architecture 
of a production enterprise system. This project is being 
created strictly as a demo project for you (and you 
know who you are).

The actual analysis to be performed for this demo is 
still under consideration depending on availability and 
quality of data as well as any insights that may be 
found on initial review of all data.


### Technology Stack
* Python 3.8
* Amazon AWS DynamoDB
* Amazon S3
* Apache Spark on Amazon AWS Elastic MapReduce (EMR)
* Amazon Redshift

### Most Important Python Libraries Used
* boto3 (Amazon AWS SDK for Python)
* PySpark
* NumPy
* Pandas
* Matplotlib

### To Be Addressed
* Security of data storage.
* Integrity of data.
* Potential bias in data.

## Specific Steps
1. The program will consume the API available at the 
US Department of Education to gather data related to
degree programs at each college and university (**COMPLETED** - 
generated CSV file of ~80 MB).
   1. The API requires paging through the results; therefore 
   the program will need to make multiple requests until all 
   necessary data is gathered.
   2. The data will be saved as a comma-separated values
      (CSV) file on AWS S3.
2. The program will consume an API from Jooble, a job posting 
aggregator website to gather the jobs available in the 
matching field of the degree program chosen in step 1 (**STATUS** - 
successfully retrieving data from Jooble. Working on pushing to 
DynamoDB).
   1. The data will be saved to the NoSQL AWS DynamoDB
      service. 
4. The data will then be retrieved from both DynamoDB 
and S3, combined, and then added to the data warehouse 
created on AWS Redshift.
5. The instance of AWS Redshift will be queried to 
retrieve the relevant data to be reviewed using Pandas. 
6. Python will then examine the data in a simplified 
way. If this were a real project, more intensive scrutiny 
would take place to look for outliers and potential bias 
in the resultant data set.
7. After processing and examination, the data will be 
visualized in Matplotlib in hopes of finding insight 
in the data. 

## Tests
Tests will be developed for the purposes of test-driven 
development (TDD) and those are TBD. Pytest and pydantic 
will be used for creating the tests and for validating the 
data.