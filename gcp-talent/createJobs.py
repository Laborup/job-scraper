import sqlite3
import re 
from gcpTalent import create_job, list_companies
from google.cloud import talent
import pprint
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import postal_address_pb2  # type: ignore


def sanitize_name(input_string):
    # Replace spaces with underscores
    sanitized_string = input_string.replace(' ', '_')
    
    # Remove special characters using regular expression
    sanitized_string = re.sub(r'[^a-zA-Z0-9_]', '', sanitized_string)
    
    # Convert to lowercase
    sanitized_string = sanitized_string.lower()
    
    return sanitized_string

def create_job_obj(company_id, job_dict):
    salaryTest = str(job_dict["salaryText"])
    custom_attribute = talent.CustomAttribute()
    custom_attribute.filterable = True
    custom_attribute.keyword_searchable = True
    custom_attribute.string_values.append(salaryTest)
    
    address_parts = [job_dict["jobLocationCity"], job_dict["jobLocationState"], job_dict["jobLocationPostal"]]
    address = ", ".join(filter(None, address_parts))

    application_info = talent.Job.ApplicationInfo()
    application_info.uris.append(job_dict["jobUrl"])
    
    pubDate = timestamp_pb2.Timestamp()
    pubDate.FromMilliseconds(int(job_dict['pubDate']))

    job = talent.Job(
        company=company_id,
        title=job_dict['jobTitle'],
        requisition_id=job_dict['jobkey'],
        description=job_dict['jobDescription'],
        language_code="en-us",
        addresses=[address], 
        application_info=application_info,
        posting_publish_time=pubDate,
        custom_attributes={"compensationText": custom_attribute},
    )
    
    return job
    
# Connect to the SQLite database
conn = sqlite3.connect('../jobs.db')
cursor = conn.cursor()
cursor.row_factory = sqlite3.Row

# Fetch all the unique values from the column

tenant_id="065a2ef4-6bf2-4341-a621-29abad6031d8"

companies = list_companies("laborup", tenant_id)


for company in companies:
    company_id = company.name.rsplit('/', 1)[-1]
    
    cursor.execute(f"SELECT * FROM jobs WHERE company = ?", (company.display_name,))
    jobs = cursor.fetchall()
    print(jobs)
    
    for job in jobs:
        job_dict = dict(job)
        
        job_obj = create_job_obj(company_id, job_dict)
        
        print(job_obj)
        
        create_job("laborup", tenant_id, company_id, job_obj)

    
    
# Close the connection
cursor.close()
conn.close()



    
