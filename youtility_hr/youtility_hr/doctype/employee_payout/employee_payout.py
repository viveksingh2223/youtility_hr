# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe, erpnext
from frappe.utils import cint, flt, nowdate, add_days, getdate, fmt_money
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words
from frappe import _
from erpnext.accounts.utils import get_fiscal_year
from frappe.utils import getdate
from frappe.model.document import Document

class EmployeePayout(Document):
	def validate(self):
		company_currency = erpnext.get_company_currency(self.company)
		self.total_in_words = money_in_words(self.total, company_currency)

	def on_update(self):
		if len(self.empdata) > 0:
			total_amount= 0.0
			for data in self.empdata:
				total_amount+= data.rounded_total
			self.total= total_amount

	def get_sal_slip_list(self, ss_status, as_dict=False):
		"""
			Returns list of salary slips based on selected criteria
		"""
		ss_list = frappe.db.sql("""
			select t1.name, t1.salary_structure from `tabSalary Slip` t1
			where t1.docstatus = %s and t1.start_date >= %s and t1.end_date <= %s
			and (t1.journal_entry is null or t1.journal_entry = "") %s
		""" % (ss_status, self.start_date, self.end_date), as_dict=as_dict)

		return ss_list

	def get_total_salary_and_loan_amounts(self):
		"""
			Get total loan principal, loan interest and salary amount from submitted salary slip based on selected criteria
		"""

		totals = frappe.db.sql("""
			select
				sum(principal_amount) as total_principal_amount,
				sum(interest_amount) as total_interest_amount,
				sum(total_loan_repayment) as total_loan_repayment,
				sum(rounded_total) as rounded_total
			from
				`tabSalary Slip` t1
			where
				t1.docstatus = 1
			and
				start_date >= %s
			and
				end_date <= %s
			""" % ('%s','%s'), (getdate(self.start_date), getdate(self.end_date)), as_dict=True)
		return totals[0]

	def get_default_payroll_payable_account(self):
		payroll_payable_account = frappe.db.get_value("Company",
			{"company_name": self.company}, "default_payroll_payable_account")

		if not payroll_payable_account:
			frappe.throw(_("Please set Default Payroll Payable Account in Company {0}")
				.format(self.company))
		return payroll_payable_account

	def make_bank_payment_entry(self):
		self.check_permission('write')
		new_total_salary_amount = 0
		default_payroll_payable_account = self.get_default_payroll_payable_account()
		for row_empdata in self.empdata:
			if row_empdata.net_pay:
				new_total_salary_amount = int(new_total_salary_amount) + int(row_empdata.net_pay)

		if new_total_salary_amount:
			journal_entry = frappe.new_doc('Journal Entry')
			journal_entry.voucher_type = 'Bank Entry'
			journal_entry.user_remark = _('Payment of salary from {0} to {1}').format(self.start_date, self.end_date)
			journal_entry.company = self.company
			journal_entry.employee_payout_ref = self.name
			journal_entry.start_date = self.start_date
			journal_entry.posting_date = nowdate()

			account_amt_list = []

			account_amt_list.append({
					"account": self.payment_account,
					"credit_in_account_currency": new_total_salary_amount
				})
			account_amt_list.append({
					"account": default_payroll_payable_account,
					"debit_in_account_currency": new_total_salary_amount
				})
			journal_entry.set("accounts", account_amt_list)
		return journal_entry.as_dict()

@frappe.whitelist()
def salary_slip_data(bank_name,start_date,end_date):
	emp_salary_data = []
	emp_data = frappe.get_all('Employee', fields=['name','employee_name','bank_name','bank_ac_no','ifsc_code'],filters={"bank_name": bank_name})
	data= frappe.db.sql("""select ssd.employee from `tabEmployee Payout` ep 
                            inner join `tabSalary Slip Data` ssd on ep.name= ssd.parent 
                            where ep.start_date>= '%s' and ep.end_date<= '%s' and ep.bank_name= '%s';"""%(start_date, end_date, bank_name), as_dict= True)
	processed_emp= []
	if len(data) >0: 
		for d in data:
			processed_emp.append(d["employee"])
	for emp_details in emp_data:
		salary_data = frappe.get_all('Salary Slip', fields=['name','bank_entry_status','net_pay','rounded_total','start_date','end_date'],filters={
			"employee": emp_details.name,
			"bank_entry_status":'Hold',
			"docstatus":1,
			"start_date":[">=", getdate(start_date)],
			"end_date":["<=", getdate(end_date)]
			})
		for sal_filter in salary_data:
			a = {
				"employee" : emp_details.name,
				"employee_name" : emp_details.employee_name,
				"ifsc_code" : emp_details.ifsc_code,
				"bank_name" : emp_details.bank_name,
				"bank_ac_no" : emp_details.bank_ac_no,
				"net_pay" : sal_filter.net_pay,
				"rounded_total" : sal_filter.rounded_total,
				"bank_entry_status" : sal_filter.bank_entry_status,
				"salary_slip_name" : sal_filter.name
			}
			if a["employee"] not in processed_emp:
				emp_salary_data.append(a)
			else:
				pass
	if len(emp_salary_data) == 0:
		frappe.msgprint("Payout Process Of All Employee Alread Done For Selected Time Period")
	return emp_salary_data
