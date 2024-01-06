import frappe
from frappe.custom.doctype.custom_field.custom_field import CustomField


# Install
def after_install():
    create_ucraft_project_id_field()


def create_ucraft_project_id_field():
    # Define the new custom field properties
    custom_field = {
        'fieldname': 'ucraft_project_id',
        'label': 'Ucraft Project ID',
        'fieldtype': 'Data',
        'insert_after': 'country',  # Adjust this based on your Company doctype layout
        # 'hidden': 1
    }

    # Add the custom field to the Company doctype
    frappe.get_doc({
        'doctype': 'Custom Field',
        'dt': 'Company',
        **custom_field
    }).insert(ignore_permissions=True)


# Uninstall
def after_uninstall():
    frappe.flags.ignore_permissions = True  # Bypass permissions
    delete_ucraft_project_id_field()
    frappe.db.commit()  # Commit the changes


def delete_ucraft_project_id_field():
    # Fetch the custom field
    custom_field = frappe.get_all('Custom Field', filters={
        'fieldname': 'ucraft_project_id',
        'dt': 'Company'
    })

    # Delete the custom field from the Company doctype
    if custom_field:
        try:
            frappe.delete_doc('Custom Field', custom_field[0].name)
        except frappe.DoesNotExistError:
            pass  # If the custom field does not exist, do nothing
