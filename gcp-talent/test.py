import os

from googleapiclient.discovery import build
from googleapiclient.errors import Error

client_service = build("jobs", "v3")


def run_sample():
    try:
        project_id = "projects/laborup"
        response = (
            client_service.projects().companies().list(parent=project_id).execute()
        )
        print("Request Id: %s" % response.get("metadata").get("requestId"))
        print("Companies:")
        if response.get("companies") is not None:
            for company in response.get("companies"):
                print("%s" % company.get("name"))
        print("")

    except Error as e:
        print("Got exception while listing companies")
        raise e


if __name__ == "__main__":
    run_sample()