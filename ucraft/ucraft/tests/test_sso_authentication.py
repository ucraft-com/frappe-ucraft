import unittest
import frappe
from frappe.utils import set_request
from ucraft.sso.auth import authenticate_login


class TestSSOAuthentication(unittest.TestCase):
    def setUp(self):
        # Setup for SSO authentication test
        self.project_id = "test_project_id"  # Example project ID
        self.window = False
        self.return_url = "http://test-return-url.com"
        self.sso_token = "test_sso_token"  # Example SSO token

        # Simulating Frappe form_dict for SSO authentication
        set_request(method='POST', path='/api/method/ucraft.ucraft.authenticate_login')
        frappe.form_dict.project_id = self.project_id
        frappe.form_dict.window = self.window
        frappe.form_dict.return_url = self.return_url
        frappe.form_dict.sso_token = self.sso_token

    def test_sso_authentication(self):
        # Test the SSO authentication process
        with frappe.get_doc('Login Manager'):
            authenticate_login(frappe.local.login_manager)

        # Check if user is logged in after SSO authentication
        self.assertNotEqual(frappe.session.user, 'Guest', 'SSO authentication failed')

    def tearDown(self):
        # Clean up after tests
        frappe.set_user('Administrator')
