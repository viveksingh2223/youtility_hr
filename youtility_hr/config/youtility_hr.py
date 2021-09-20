from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
			{
                "label": _("Youtility HR"),
                "items": [
					{
						"type": "doctype",
                        "name": "Salary Structure",
					},
					{
                        "type": "doctype",
                        "name": "Salary Structure Assignment",
                    },
					{
                        "type": "doctype",
                        "name": "Loan",
                    },
					{
                        "type": "doctype",
                        "name": "Payroll Entry",
                    },
                    {
                        "type": "doctype",
                        "name": "Employee Payout",
                    }
                ]
            },
			{
				"label": _("Youtility Accounts"),
				"items": [
					{
						"type": "doctype",
						"name": "Business Unit",
					},
					{
						"type": "doctype",
						"name": "Sales Order",
					},
					{
                        "type": "doctype",
                        "name": "Sales Invoice",
                    },
					{
                        "type": "doctype",
                        "name": "Auto Repeat",
                    }
				]
			}
		]
