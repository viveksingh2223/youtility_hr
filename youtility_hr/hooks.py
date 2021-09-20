# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "youtility_hr"
app_title = "Youtility HR"
app_publisher = "Vivek Singh"
app_description = "Custom App for Youtility Payroll"
app_icon = "octicon octicon-file-directory"
app_color = "'blue'"
app_email = "vivek.singh@youtility.in"
app_license = "MIT"


fixtures= [{
                "dt": "Custom Field",
                "filters": [["name", "in", [
                            "Issue-issue_category",
							"Customer-customer_code",
							"Sales Order-client",
							"Sales Order-site",
							"Sales Invoice-client",
							"Sales Invoice-site"
                           ]]]
}]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/youtility_hr/css/youtility_hr.css"
# app_include_js = "/assets/youtility_hr/js/youtility_hr.js"

# include js, css files in header of web template
# web_include_css = "/assets/youtility_hr/css/youtility_hr.css"
# web_include_js = "/assets/youtility_hr/js/youtility_hr.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "youtility_hr.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "youtility_hr.install.before_install"
# after_install = "youtility_hr.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "youtility_hr.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"youtility_hr.tasks.all"
# 	],
# 	"daily": [
# 		"youtility_hr.tasks.daily"
# 	],
# 	"hourly": [
# 		"youtility_hr.tasks.hourly"
# 	],
# 	"weekly": [
# 		"youtility_hr.tasks.weekly"
# 	]
# 	"monthly": [
# 		"youtility_hr.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "youtility_hr.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "youtility_hr.event.get_events"
# }

