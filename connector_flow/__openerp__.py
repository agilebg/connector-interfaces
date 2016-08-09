# -*- coding: utf-8 -*-
# Copyright (C) 2014 initOS GmbH & Co. KG (<http://www.initos.com>).
# Copyright (C) 2016 Agile business group (<http://www.agilebg.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Connector-based task flow for import/export',
    'version': '9.0.1.0.0',
    'category': 'Connector',
    'author': 'initOS GmbH & Co. KG,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'http://www.initos.com',
    'depends': [
        'connector',
    ],
    'external_dependencies': {
        'python': ['ftputil'],
    },
    'data': [
        'views/impexp_task_view.xml',
        'views/file_view.xml',
        'views/chunk_view.xml',
        'wizards/run_task_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
