# -*- coding: utf-8 -*-
# Copyright (C) 2014 initOS GmbH & Co. KG (<http://www.initos.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api
from .abstract_task import AbstractTask

from base64 import b64decode
import csv
import simplejson
import logging
_logger = logging.getLogger(__name__)


class TableRowImport(AbstractTask):
    def _row_generator(self, file_data, config=None):
        """Parses a given blob into rows; returns an iterator to rows.
           Has to be implemented in derived classes."""
        raise Exception("Not Implemented")

    def run(self, config=None, file_id=None, async=True, **kwargs):
        if not file_id:
            return

        includes_header = config.get('includes_header', False)

        lineno = 0
        header = None
        file = self.session.env['impexp.file'].browse(file_id)
        rows = self._row_generator(b64decode(file.attachment_id.datas),
                                   config=config)
        for row in rows:
            lineno += 1
            if includes_header and lineno == 1:
                header = row
                continue
            if not row:
                continue
            name = '%s, line %d' % (file.attachment_id.datas_fname, lineno)
            data = row
            if header:
                data = dict(zip(header, data))
            chunk_id = self.session.env['impexp.chunk'].create(
                                           {'name': name,
                                            'data': simplejson.dumps(data),
                                            'file_id': file.id}).id
            self.run_successor_tasks(
                chunk_id=chunk_id, async=async, file_id=file.id, **kwargs)
            if lineno % 1000 == 0:
                _logger.info('Created %d chunks', lineno)

        file.write({'state': 'done'})


class CsvImport(TableRowImport):
    """Parses a CSV file and stores the lines as chunks"""

    def _row_generator(self, file_data, config=None):
        encoding = config.get('encoding', 'utf-8')
        data = file_data.decode(encoding)\
                        .encode('utf-8')\
                        .split("\n")
        return csv.reader(data)


class CsvImportTask(models.Model):
    _inherit = 'impexp.task'

    @api.model
    def _get_available_tasks(self):
        return super(CsvImportTask, self)._get_available_tasks() + [
            ('csv_import', 'CSV Import')]

    def csv_import_class(self):
        return CsvImport
