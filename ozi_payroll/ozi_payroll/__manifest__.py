# -*- coding: utf-8 -*-
{
    'name': "OZI Payroll",

    'summary': """
        Customization On Payroll""",

    'description': """
        Customization On Payroll
    """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'hr',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_attendance', 'hr_payroll', 'hr_contract'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_config_setting_views.xml',
        'views/hr_attendance_views.xml',
        'views/hr_contract.xml',
    ],

}
