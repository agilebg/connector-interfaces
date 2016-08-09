# -*- coding: utf-8 -*-
# Copyright (C) 2014 initOS GmbH & Co. KG (<http://www.initos.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ImpExpChunk(models.Model):
    _name = 'impexp.chunk'
    _description = ('Structured (parsed) data from a file'
                    ' to be imported/exported')

    @api.model
    def _states(self):
        return [('new', 'New'),
                ('failed', 'Failed'),
                ('done', 'Done')]

    file_id = fields.Many2one('impexp.file', string='File')
    name = fields.Char(string='Name', required=True)
    data = fields.Text(string='Data', required=True)
    task_id = fields.Many2one(string='Related Task', related='file_id.task_id')
    state = fields.Selection(string='State', selection='_states',
                             default='new')
