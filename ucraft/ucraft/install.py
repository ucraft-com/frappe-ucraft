import frappe


def after_install():
    create_ucraft_project_id_field()


def create_ucraft_project_id_field():
    # Define the new custom field properties
    custom_field = {
        'fieldname': 'ucraft_project_id',
        'label': 'Ucraft Project ID',
        'fieldtype': 'Data',
        'insert_after': 'country',  # Adjust this based on your Company doctype layout
        'hidden': 1
    }

    # Add the custom field to the Company doctype
    frappe.get_doc({
        'doctype': 'Custom Field',
        'dt': 'Company',
        **custom_field
    }).insert(ignore_permissions=True)
