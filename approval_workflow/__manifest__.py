# -*- coding: utf-8 -*-
{
    'name': "Approval Workflow",

    'summary': """
        Approval Workflow on Payments""",

    'description': """
        Approval Workflow on Payments
    """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'hr_payroll'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/account_move_views.xml',
        'views/account_payment_views.xml',
        'views/hr_payroll_views.xml',
    ],

}
