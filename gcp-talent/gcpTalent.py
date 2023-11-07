from google.cloud import talent

tenant_id = '065a2ef4-6bf2-4341-a621-29abad6031d8'


def list_tenants(project_id):
    """List Tenants"""

    client = talent.TenantServiceClient()

    # project_id = 'Your Google Cloud Project ID'

    if isinstance(project_id, bytes):
        project_id = project_id.decode("utf-8")
    parent = f"projects/{project_id}"

    # Iterate over all results
    for response_item in client.list_tenants(parent=parent):
        print(f"Tenant Name: {response_item.name}")
        print(f"External ID: {response_item.external_id}")


def create_tenant(project_id, external_id):
    """Create Tenant for scoping resources, e.g. companies and jobs"""

    client = talent.TenantServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # external_id = 'Your Unique Identifier for Tenant'

    if isinstance(project_id, bytes):
        project_id = project_id.decode("utf-8")
    if isinstance(external_id, bytes):
        external_id = external_id.decode("utf-8")
    parent = f"projects/{project_id}"
    tenant = talent.Tenant(external_id=external_id)

    response = client.create_tenant(parent=parent, tenant=tenant)
    print("Created Tenant")
    print(f"Name: {response.name}")
    print(f"External ID: {response.external_id}")
    return response.name

def create_company(project_id, tenant_id, display_name, external_id):
    """Create Company"""

    client = talent.CompanyServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # display_name = 'My Company Name'
    # external_id = 'Identifier of this company in my system'

    if isinstance(project_id, bytes):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, bytes):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(display_name, bytes):
        display_name = display_name.decode("utf-8")
    if isinstance(external_id, bytes):
        external_id = external_id.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"
    company = {"display_name": display_name, "external_id": external_id}

    response = client.create_company(parent=parent, company=company)
    print("Created Company")
    print(f"Name: {response.name}")
    print(f"Display Name: {response.display_name}")
    print(f"External ID: {response.external_id}")
    return response.name

def list_companies(project_id, tenant_id):
    """List Companies"""

    client = talent.CompanyServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'

    if isinstance(project_id, bytes):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, bytes):
        tenant_id = tenant_id.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"

    # Iterate over all results
    results = []
    for company in client.list_companies(parent=parent):
        results.append(company)
        #print(f"Company Name: {company.name}")
        #print(f"Display Name: {company.display_name}")
        #print(f"External ID: {company.external_id}")
    return results

from google.cloud import talent

def get_job(project_id, tenant_id, job_id):
    """Get Job"""

    client = talent.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # job_id = 'Job ID'

    if isinstance(project_id, bytes):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, bytes):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(job_id, bytes):
        job_id = job_id.decode("utf-8")
    name = client.job_path(project_id, tenant_id, job_id)

    response = client.get_job(name=name)

def create_job(project_id, tenant_id, company_id, job):
    """Create Job with Custom Attributes"""

    client = talent.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # company_id = 'Company name, e.g. projects/your-project/companies/company-id'
    # requisition_id = 'Job requisition ID, aka Posting ID. Unique per job.'
    # language_code = 'en-US'

    if isinstance(project_id, bytes):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, bytes):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(company_id, bytes):
        company_id = company_id.decode("utf-8")

    # Custom attribute can be string or numeric value,
    # and can be filtered in search queries.
    # https://cloud.google.com/talent-solution/job-search/docs/custom-attributes

    parent = f"projects/{project_id}/tenants/{tenant_id}"

    try:
        response = client.create_job(parent=parent, job=job)
        print(f"Created job: {response.name}")
        return response.name
    except Exception as e:
        print(f"Error creating job: {e}")
        return None


def list_jobs(project_id, tenant_id, filter_):
    """List Jobs"""

    client = talent.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # filter_ = 'companyName=projects/my-project/companies/company-id'

    if isinstance(project_id, bytes):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, bytes):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(filter_, bytes):
        filter_ = filter_.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"

    # Iterate over all results
    results = []
    for job in client.list_jobs(parent=parent, filter=filter_):
        results.append(job.name)
        print("Job name: {job.name}")
        print("Job requisition ID: {job.requisition_id}")
        print("Job title: {job.title}")
        print("Job description: {job.description}")
    return results
