# -*- coding: utf-8 -*-
# Copyright (c) 2018, TUSHAR TAJNE and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.contacts.address_and_contact import load_address_and_contact, delete_contact_and_address
from frappe import _

class BusinessUnit(Document):
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

	def validate(self):
		name = str(self.bu_code).upper()
		self.name = _(name)
	def on_trash(self):
		delete_contact_and_address('Buisness Unit', self.name)
		if frappe.db.exists("Customer", self.bu_name):
			frappe.delete_doc("Customer", frappe.db.exists("Customer", self.bu_name))
	def create_primary_address(self):
		if self.flags.is_new_doc and self.get('address_line1'):
			make_address(self)

	def on_update(self):
		# create customer from bu type customer
		self.create_primary_address()
		if self.bu_type == "Client":
			exist_list=frappe.get_all('Customer', filters={'customer_code': self.bu_code}, fields=['name', 'customer_name'])
			if not exist_list:
				customer = frappe.new_doc("Customer")
				customer.customer_code = self.bu_code
				customer.customer_name = self.bu_name
				if self.status == "Active":	customer.disabled = 0
				else: customer.disabled = 1
				customer.customer_type = "Company"
				customer.customer_group = "Commercial"
				customer.flags.ignore_permissions = self.flags.ignore_permissions
				customer.autoname()
				if not frappe.db.exists("Customer", self.bu_name):
					customer.insert()
			else:
				doc = frappe.get_doc("Customer", exist_list[0]["name"])	
				doc.customer_code = self.bu_code
				doc.customer_name = self.bu_name
				if self.status == "Active":	doc.disabled = 0
				else:doc.disabled = 1
				doc.flags.ignore_permissions = self.flags.ignore_permissions
				doc.save()

@frappe.whitelist()
def get_children(doctype, parent, bu_type, is_root=False):
	#parent_fieldname = 'parent_' + doctype.lower().replace(' ', '_')
	parent_fieldname = 'business_unit'
	fields = [
		'name as value','bu_type as type',
		'is_group as expandable'
	]
	filters = [['docstatus', '<', 2]]
	if is_root:
		fields += ['bu_type'] if doctype == 'Business Unit' else []
		filters.append(['ifnull(`{0}`,"")'.format(parent_fieldname), '=', '' if is_root else parent])
		filters.append(['bu_type', '=', bu_type])
	else:
		parent_fieldname2 = 'business_unit'
		filters.append(['ifnull(`{0}`,"")'.format(parent_fieldname2), '=', '' if is_root else parent])
	acc = frappe.get_list(doctype, fields=fields, filters=filters)
	return acc

def make_address(args, is_primary_address=1):
	address = frappe.get_doc({
		'doctype': 'Address',
		'address_title': args.get('name'),
		'address_line1': args.get('address_line1'),
		'address_line2': args.get('address_line2'),
		'city': args.get('city'),
		'state': args.get('state'),
		'pincode': args.get('pincode'),
		'country': args.get('country'),
		'links': [{
			'link_doctype': args.get('doctype'),
			'link_name': args.get('name')
		}]
	}).insert()

	return address
