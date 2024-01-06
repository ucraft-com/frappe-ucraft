# import unittest
# import frappe
# from ucraft.ucraft.api import create_company_for_ucraft_project
#
#
# class TestCreateCompanyForUcraftProject(unittest.TestCase):
#     def setUp(self):
#         frappe.connect("dev.com")
#         # Set up necessary data for each test
#         self.data = {
#             'project_id': 'test_project_id',
#             'company_name': 'test_company'
#         }
#
#     def test_missing_fields(self):
#         # Test case: missing fields in the request data
#         data = {}
#         response = create_company_for_ucraft_project(data)
#         self.assertEqual(response, {'message': 'Missing required fields', 'status': 400})
#
#     def test_existing_company(self):
#         # Test case: a company with the given project ID already exists
#         existing_company_name = 'existing_company'
#         # Insert an existing company into the database
#         doc = frappe.get_doc({
#             'doctype': 'Company',
#             'company_name': existing_company_name,
#             'ucraft_project_id': self.data['project_id']
#         })
#         doc.insert()
#         response = create_company_for_ucraft_project(self.data)
#         self.assertEqual(response, {'message': 'Company already exists for this project ID', 'status': 409})
#         # Clean up: remove the inserted document
#         frappe.delete_doc('Company', existing_company_name)
#
#     def test_successful_creation(self):
#         # Test case: successful company creation
#         response = create_company_for_ucraft_project(self.data)
#         self.assertEqual(response,
#                          {'message': f"Company {self.data['company_name']} created successfully", 'status': 200})
#         # Clean up: remove the created company
#         frappe.delete_doc('Company', self.data['company_name'])
#
#     def tearDown(self):
#         frappe.local.rollback()
#         frappe.local.disconnect()
