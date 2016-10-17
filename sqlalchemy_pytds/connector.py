# connectors/pytds.py

from sqlalchemy.connectors import Connector
from sqlalchemy.util import asbool

import sys
import re
import pytds

prevexecute = pytds.Cursor.execute
def execute(self, operation, params=()):
    if operation[:3] == 'sp_':
        proc, operation = operation.split(' ', 1)
        assert proc == 'sp_columns'
        operation = operation.split("'")
        params = {
            '@table_name': operation[1],
            '@table_owner': operation[3],
        }
        return pytds.Cursor.callproc(self, proc, params)
    return prevexecute(self, operation, params)
pytds.Cursor.execute = execute

class PyTDSConnector(Connector):
    driver = 'pytds'

    supports_sane_multi_rowcount = False
    supports_unicode = True
    supports_unicode_binds = True
    supports_unicode_statements = True
    supports_native_decimal = True
    default_paramstyle = 'pyformat'

    @classmethod
    def dbapi(cls):
        return pytds

    def is_disconnect(self, e, connection, cursor):
        if isinstance(e, self.dbapi.ProgrammingError):
            return "The cursor's connection has been closed." in str(e) or \
                            'Attempt to use a closed connection.' in str(e)
        elif isinstance(e, self.dbapi.Error):
            return '[08S01]' in str(e)
        else:
            return False

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username='user')
        opts.update(url.query)

        keys = opts
        query = url.query

        connect_args = {}
        for param in ('autocommit', 'use_mars', 'as_dict'):
            if param in keys:
                connect_args[param] = asbool(keys.pop(param))
        for param in ('port', 'timeout', 'login_timeout'):
            if param in keys:
                connect_args[param] = int(keys.pop(param))
        for param in ('host', 'user', 'password', 'database'):
            if param in keys:
                connect_args[param] = keys.pop(param)
        connect_args['server'] = connect_args['host']
        del connect_args['host']

        return [[], connect_args]

    def _dbapi_version(self):
        if not self.dbapi:
            return ()
        return self._parse_dbapi_version(self.dbapi.version)

    def _parse_dbapi_version(self, vers):
        m = re.match(
                r'(?:py.*-)?([\d\.]+)(?:-(\w+))?',
                vers
            )
        if not m:
            return ()
        vers = tuple([int(x) for x in m.group(1).split(".")])
        if m.group(2):
            vers += (m.group(2),)
        return vers

    def _get_server_version_info(self, connection):
        l = connection.connection.product_version
        version = []
        for i in range(4):
            version.append(l&0xff)
            l >>= 8
        version.reverse()
        return tuple(version)
