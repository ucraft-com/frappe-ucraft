import frappe
import requests

from .constants import MAIN_URL_UCRAFT


def authenticate_login(login_manager):
    # Check if the user is already logged in
    if frappe.session.user != 'Guest':
        return

    # Extract the project ID and other necessary parameters
    project_id = frappe.form_dict.get('project_id')
    window = frappe.form_dict.get('window')
    return_url = frappe.form_dict.get('return_url')

    # Redirect to SSO login page if not authenticated
    if not frappe.form_dict.get('sso_token'):
        redirect_to_sso_login(project_id, return_url)
        return

    # Verify the SSO token after the user is redirected back from SSO login
    sso_token = frappe.form_dict.get('sso_token')
    user_data = verify_sso_token(sso_token, project_id, window)

    if user_data:
        # Get the company based on project ID, return error if not found
        company = get_company_by_project_id(project_id)
        if not company:
            frappe.throw(f"No company found for project ID {project_id}")

        # Create or update the user in db
        create_or_update_user(user_data, company)

        # Log the user into db
        frappe.set_user(user_data['email'])
        frappe.local.login_manager.post_login()


def redirect_to_sso_login(project_id, return_url):
    # Redirect the user to the SSO login page
    login_url = f'{MAIN_URL_UCRAFT}/login?project_id={project_id}&return_url={return_url}'
    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = login_url


def verify_sso_token(token, project_id, window):
    try:
        callback_url = f'/callback?project_id={project_id}&window={window}'
        response = requests.post(callback_url, json={'token': token})

        response.raise_for_status()  # Raises a HTTPError if the response status code is 4XX or 5XX

        return response.json()
    except requests.exceptions.RequestException as e:
        frappe.log_error(message=f"Failed to verify SSO token: {e}", title="SSO Token Verification Error")
        return None


def get_company_by_project_id(project_id):
    # Check if a company with the given project ID exists
    return frappe.db.get_value('Company', {'ucraft_project_id': project_id}, 'name')


def create_or_update_user(user_data, company):
    user_email = user_data['email']

    if not frappe.db.exists('User', user_email):
        # Create a new user if it doesn't exist
        new_user = frappe.get_doc({
            'doctype': 'User',
            'email': user_email,
            'first_name': user_data.get('first_name', ''),
            'enabled': 1,
            'new_password': user_data.get('password', frappe.generate_hash(user_email)),
            # Add other fields as necessary
        })
        new_user.insert()
        # Set default company for the user
        new_user.append('user_companies', {
            'company': company
        })
        new_user.save()
