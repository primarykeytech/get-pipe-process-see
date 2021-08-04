from extract import doe
from careers import job_data


def main():
    # print("Hello World!")
    # doe_data = doe.get_api_data()
    # job_data.get_jobs_data()
    job_data.api_call("software", "Seattle")
    print("data retrieved")


if __name__ == "__main__":
    main()
