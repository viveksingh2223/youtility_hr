// Copyright (c) 2018, TUSHAR TAJNE and contributors
// For license information, please see license.txt

frappe.ui.form.on('Business Unit', {
	refresh:function(frm){
		frappe.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Business Unit'}
		frm.toggle_display(['address_html'], !frm.doc.__islocal);
		if(!frm.doc.__islocal) {
				frappe.contacts.render_address_and_contact(frm);
		}else {
				frappe.contacts.clear_address_and_contact(frm);
			}

	},
    add_toolbar_buttons: function(frm) {
		frm.add_custom_button(__('Business Unit'),
			function () { frappe.set_route("Tree", "Business Unit"); });
    },
    bu_type: function(frm){
		cur_frm.doc.business_unit= ""
		frm.refresh_field("business_unit")
	    frm.events.business_unit(frm);
    },
    business_unit: function(frm){
        frm.set_df_property("business_unit", "reqd", 1)
        frm.refresh_field("business_unit");

        if(frm.doc.bu_type == "Client"){
            frm.set_value("is_group", 1)
            frm.refresh_field("is_group")
            frm.set_df_property("business_unit", "reqd", 0)
            refresh_field("business_unit");
            cur_frm.fields_dict.business_unit.get_query = function(doc) {
                        return {
                            filters: [
                                ["Business Unit", "bu_type", "in", ["None"]]
                            ]
                        }
                    }
                    frm.refresh_field("business_unit");
        }
        if(frm.doc.bu_type == "Customer"){
            frm.set_value("is_group", 1)
            frm.refresh_field("is_group")
            cur_frm.fields_dict.business_unit.get_query = function(doc) {
                return {
                    filters: [
                        ["Business Unit", "bu_type", "in", ["Client"]]
                    ]
                }
            }
            frm.refresh_field("business_unit");
        }
        if(frm.doc.bu_type == "Site"){
            frm.set_value("is_group", 0)
            frm.refresh_field("is_group")
            cur_frm.fields_dict.business_unit.get_query = function(doc) {
                return {
                    filters: [
                        ["Business Unit", "bu_type", "in", ["Client", "Customer"]]
                    ]
                }
            }
            frm.refresh_field("business_unit");
        }
    }
});

