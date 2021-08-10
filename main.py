from extract import doe
from careers import job_data
from dba.dynamodb import dyn_crud

def main():
    # print("Hello World!")
    # doe_data = doe.get_api_data()
    # job_data.get_jobs_data()
    job_data.api_call("teacher", "Seattle")
    # dyn_crud.retrieve_record('33ef91be-f5b3-11eb-9120-a0d3c15425c1')
    # dyn_crud.retrieve_record_by_location_title('Daly City, CA', 'Staff Nurse I')
    # dyn_crud.delete_record('from-test-dyndb')
    print("data retrieved")


if __name__ == "__main__":
    main()
