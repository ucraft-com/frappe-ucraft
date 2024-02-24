# Copyright (c) 2024, Webisoft and contributors
# For license information, please see license.txt
from pprint import pprint

# import frappe
from frappe.model.document import Document


class KafkaConfiguration(Document):
    def get_active_events_list(self):
        events = []
        if self.send_on_update:
            events.append("on_update")
        if self.send_on_cancel:
            events.append("on_cancel")
        if self.send_on_trash:
            events.append("on_trash")
        if self.send_on_submit:
            events.append("on_submit")
        if self.send_before_insert:
            events.append("before_insert")
        if self.send_after_insert:
            events.append("after_insert")
        if self.send_before_save:
            events.append("before_save")
        if self.send_after_save:
            events.append("after_save")
        if self.send_before_rename:
            events.append("before_rename")
        if self.send_after_rename:
            events.append("after_rename")
        if self.send_before_cancel:
            events.append("before_cancel")
        if self.send_after_cancel:
            events.append("after_cancel")
        if self.send_before_trash:
            events.append("before_trash")
        if self.send_after_trash:
            events.append("after_trash")
        if self.send_before_restore:
            events.append("before_restore")
        if self.send_after_restore:
            events.append("after_restore")
        if self.send_before_delete:
            events.append("before_delete")
        if self.send_after_delete:
            events.append("after_delete")

        return events

    def is_in_active_doctypes(self, doctype):
        return doctype in [obj.as_dict()['method_name'] for obj in self.objects_to_sync]

    def should_execute(self, doc_name, method_name):
        if self.is_in_active_doctypes(doc_name) and method_name in self.get_active_events_list():
            return True
        return False
