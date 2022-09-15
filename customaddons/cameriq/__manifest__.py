# -*- coding: utf-8 -*-
{
    'name': "Cameriq",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Cameriq",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/pegawai_view.xml',
        'views/client_view.xml',
        'views/menu.xml',
        'wizard/update_biaya_wizard_view.xml',
        'wizard/update_stok_wizard_view.xml',
        'views/barang_view.xml',
        'views/kategori_view.xml',
        'views/transaksi_view.xml',
        'report/report_cameriq_transaksi.xml',
        'report/report.xml',
        'report/wizard_transaksireport_template.xml',
        'report/wizard_barangreport_template.xml',
        'wizard/transaksireport_wizard_view.xml',
        'wizard/barangreport_wizard_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
