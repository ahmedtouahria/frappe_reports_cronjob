# Copyright (c) 2023, ahmedtouahria and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document


class SalesFinanceReport(Document):
    def after_insert(self):
        frappe.sendmail(recipients=["ahmedtouahria2001@gmail.com"], message="Thank you for registering!")
