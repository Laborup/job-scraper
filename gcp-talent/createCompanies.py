import sqlite3
import re 
from gcpTalent import create_company

def sanitize_company_name(input_string):
    # Replace spaces with underscores
    sanitized_string = input_string.replace(' ', '_')
    
    # Remove special characters using regular expression
    sanitized_string = re.sub(r'[^a-zA-Z0-9_]', '', sanitized_string)
    
    # Convert to lowercase
    sanitized_string = sanitized_string.lower()
    
    return sanitized_string


# Connect to the SQLite database
conn = sqlite3.connect('../jobs.db')
cursor = conn.cursor()

# Replace 'your_table' with the actual table name and 'your_column' with the actual column name
query = 'SELECT DISTINCT company FROM jobs'

# Execute the query
cursor.execute(query)

# Fetch all the unique values from the column
companies = cursor.fetchall()

# Close the connection
conn.close()

for company in companies:
    project_id = 'laborup'
    tenant_id = '065a2ef4-6bf2-4341-a621-29abad6031d8'
    display_name = company[0]
    external_id = sanitize_company_name(company[0])
    
    create_company(project_id, tenant_id, display_name, external_id)