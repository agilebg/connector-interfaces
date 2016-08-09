# -*- coding: utf-8 -*-
# Copyright (C) 2014 initOS GmbH & Co. KG (<http://www.initos.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, api
from .abstract_task import AbstractTask
from base64 import b64decode
import ftputil
import ftputil.session
import logging
_logger = logging.getLogger(__name__)


class FtpUpload(AbstractTask):
    """FTP Configuration options:
     - host, user, password, port
     - upload_directory:  directory on the FTP server where files are
                          uploaded to
    """

    def _handle_existing_target(self, ftp_conn, target_name, filedata):
        raise Exception("%s already exists" % target_name)

    def _handle_new_target(self, ftp_conn, target_name, filedata):
        with ftp_conn.open(target_name, mode='wb') as fileobj:
            fileobj.write(filedata)
            _logger.info('wrote %s, size %d', target_name, len(filedata))

    def _target_name(self, ftp_conn, upload_directory, filename):
        return upload_directory + '/' + filename

    def _upload_file(self, config, filename, filedata):
        ftp_config = config['ftp']
        upload_directory = ftp_config.get('upload_directory', '')
        port_session_factory = ftputil.session.session_factory(
            port=int(ftp_config.get('port', 21))
            )
        with ftputil.FTPHost(ftp_config['host'], ftp_config['user'],
                             ftp_config['password'],
                             session_factory=port_session_factory) as ftp_conn:
            target_name = self._target_name(ftp_conn,
                                            upload_directory,
                                            filename)
            if ftp_conn.path.isfile(target_name):
                self._handle_existing_target(ftp_conn, target_name, filedata)
            else:
                self._handle_new_target(ftp_conn, target_name, filedata)

    def run(self, config=None, file_id=None, async=True):
        f = self.session.env['impexp.file'].browse(file_id)
        self._upload_file(config, f.attachment_id.datas_fname,
                          b64decode(f.attachment_id.datas))


class FtpUploadTask(models.Model):
    _inherit = 'impexp.task'

    @api.model
    def _get_available_tasks(self):
        return super(FtpUploadTask, self)._get_available_tasks() + [
            ('ftp_upload', 'FTP Upload')]

    def ftp_upload_class(self):
        return FtpUpload
