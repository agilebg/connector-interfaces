# -*- coding: utf-8 -*-
# Copyright (C) 2014 initOS GmbH & Co. KG (<http://www.initos.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, api
from .abstract_task import AbstractChunkReadTask
from cStringIO import StringIO

import csv


class CsvExport(AbstractChunkReadTask):
    "Reads a chunk and writes it into a CSV file"

    def read_chunk(self, config=None, chunk_data=None, async=True):
        if not chunk_data:
            return

        # output encoding defaults to utf-8
        encoding = config.get('encoding', 'utf-8')

        def encode_value(value):
            if isinstance(value, unicode):
                return value.encode(encoding)
            return value

        data = StringIO()
        writer = csv.writer(data)
        for row in chunk_data:
            writer.writerow(map(encode_value, row))

        file_id = self.create_file(config.get('filename'), data.getvalue())
        result = self.run_successor_tasks(file_id=file_id, async=async)
        if result:
            return result
        return file_id


class CsvExportTask(models.Model):
    _inherit = 'impexp.task'

    @api.model
    def _get_available_tasks(self):
        return super(CsvExportTask, self)._get_available_tasks() + [
            ('csv_export', 'CSV Export')]

    def csv_export_class(self):
        return CsvExport
