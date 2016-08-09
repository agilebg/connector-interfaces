# -*- coding: utf-8 -*-
# Copyright (C) 2014 initOS GmbH & Co. KG (<http://www.initos.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, fields, api


class ImpExpFile(models.Model):
    _name = 'impexp.file'
    _description = 'Wrapper for a file to be imported/exported'
    _rec_name = 'attachment_id'

    @api.model
    def _states(self):
        return [('new', 'New'),
                ('failed', 'Failed'),
                ('done', 'Done')]

    attachment_id = fields.Many2one('ir.attachment', string='Attachment',
                                    required=True)
    task_id = fields.Many2one('impexp.task', string='Task')
    state = fields.Selection(string='State', selection='_states',
                             default='new', required=True)
