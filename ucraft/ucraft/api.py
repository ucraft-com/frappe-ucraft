import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def create_company_for_ucraft_project():
    # Ensure that the request is valid and has the necessary data
    data = frappe.parse_json(frappe.request.data)
    if 'project_id' not in data or 'company_name' not in data:
        return {'message': 'Missing required fields', 'status': 400}

    project_id = data['project_id']
    company_name = data['company_name']

    # Check if a company with the given project ID already exists
    existing_company = frappe.db.get_value('Company', {'ucraft_project_id': project_id}, 'name')
    if existing_company:
        return {'message': 'Company already exists for this project ID', 'status': 409}

    # Create a new company
    new_company = frappe.get_doc({
        'doctype': 'Company',
        'company_name': company_name,
        'ucraft_project_id': project_id  # Ensure this custom field exists in the Company doctype
    })
    new_company.insert()

    return {'message': f'Company {company_name} created successfully', 'status': 200}
