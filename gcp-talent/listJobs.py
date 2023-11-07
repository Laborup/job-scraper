from gcpTalent import list_jobs, list_companies

tenant_id="065a2ef4-6bf2-4341-a621-29abad6031d8"

companies = list_companies("laborup", tenant_id)

for company in companies:
    company_id = company.name.rsplit('/', 1)[-1]

    filter = 'companyName="projects/laborup/companies/' + company_id + '"'

    list_jobs("laborup", "065a2ef4-6bf2-4341-a621-29abad6031d8", filter_=filter)
