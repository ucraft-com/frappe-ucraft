# Copyright (c) 2024, Webisoft and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class KafkaConfiguration(Document):
    def get_active_events_list(self):
        events = []
        if self.on_update:
            events.append("on_update")
        if self.on_cancel:
            events.append("on_cancel")
        if self.on_trash:
            events.append("on_trash")
        if self.on_submit:
            events.append("on_submit")
        if self.before_insert:
            events.append("before_insert")
        if self.after_insert:
            events.append("after_insert")
        if self.before_save:
            events.append("before_save")
        if self.after_save:
            events.append("after_save")
        if self.before_rename:
            events.append("before_rename")
        if self.after_rename:
            events.append("after_rename")
        if self.before_cancel:
            events.append("before_cancel")
        if self.after_cancel:
            events.append("after_cancel")
        if self.before_trash:
            events.append("before_trash")
        if self.after_trash:
            events.append("after_trash")
        if self.before_restore:
            events.append("before_restore")
        if self.after_restore:
            events.append("after_restore")
        if self.before_delete:
            events.append("before_delete")
        if self.after_delete:
            events.append("after_delete")
        if self.not_found:
            events.append("not_found")
        return events

    def is_in_active_doctypes(self, doctype):
        return doctype in self.objects_to_sync.split(',')

    def should_execute(self, doc_name, method_name):
        if self.is_in_active_doctypes(doc_name) and method_name in self.get_active_events_list():
            return True
        return False
