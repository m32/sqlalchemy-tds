# connectors/pytds.py
import pytds.login
from sqlalchemy.connectors import Connector
from sqlalchemy.util import asbool

import re
import pytds
from pytds import tds

prevexecute = pytds.Cursor.execute


def execute(self, operation, params=None):
    #print('execute:', operation, params)
    if operation[:15] == "EXEC sp_columns":
        proc = "sp_columns"
        params = {
            "@table_name": params["table_name"],
            "@table_owner": params["table_owner"],
        }
        return pytds.Cursor.callproc(self, proc, params)
    elif operation[:10] == "sp_columns":
        proc = "sp_columns"
        params = {
            "@table_name": params["table_name"],
            "@table_owner": params["table_owner"],
        }
        return pytds.Cursor.callproc(self, proc, params)
    return prevexecute(self, operation, params)


pytds.Cursor.execute = execute


def process_tabname(self):
    r = self._reader
    total_length = r.get_smallint()
    if not tds.tds_base.IS_TDS71_PLUS(self):
        name_length = r.get_smallint()
    tds.skipall(r, total_length)


def process_colinfo(self):
    r = self._reader
    total_length = r.get_smallint()
    tds.skipall(r, total_length)


tds._token_map.update(
    {
        tds.tds_base.TDS_TABNAME_TOKEN: lambda self: process_tabname(self),
        tds.tds_base.TDS_COLINFO_TOKEN: lambda self: process_colinfo(self),
    }
)


class PyTDSConnector(Connector):
    driver = "pytds"

    supports_sane_multi_rowcount = False
    supports_unicode = True
    supports_unicode_binds = True
    supports_unicode_statements = True
    supports_native_decimal = True
    default_paramstyle = "pyformat"

    @classmethod
    def dbapi(cls):
        return pytds

    def is_disconnect(self, e, connection, cursor):
        if isinstance(e, self.dbapi.ProgrammingError):
            return "The cursor's connection has been closed." in str(
                e
            ) or "Attempt to use a closed connection." in str(e)
        elif isinstance(e, self.dbapi.Error):
            return "[08S01]" in str(e)
        else:
            return False

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username="user")
        opts.update(url.query)

        keys = opts
        query = url.query

        connect_args = {}
        for param in ("autocommit", "use_mars", "as_dict"):
            if param in keys:
                connect_args[param] = asbool(keys.pop(param))
        for param in ("port", "timeout", "login_timeout"):
            if param in keys:
                connect_args[param] = int(keys.pop(param))
        for param in ("host", "user", "password", "database", "auth_method"):
            if param in keys:
                connect_args[param] = keys.pop(param)

        connect_args["dsn"] = connect_args.pop("host", "localhost")

        if "auth_method" in connect_args:
            if connect_args["auth_method"] == "mssql":
                del connect_args["auth_method"]
            elif connect_args["auth_method"] == "ntlm":
                connect_args["auth"] = pytds.login.NtlmAuth(
                    connect_args["user"], connect_args["password"]
                )
                del connect_args["auth_method"]
                del connect_args["user"]
                del connect_args["password"]
            elif connect_args["auth_method"] == "sso":
                connect_args["use_sso"] = True
                del connect_args["auth_method"]
            else:
                raise Exception("Unknown auth_method " + connect_args["auth_method"])

        return [[], connect_args]

    def _dbapi_version(self):
        if not self.dbapi:
            return ()
        return self._parse_dbapi_version(self.dbapi.version)

    def _parse_dbapi_version(self, vers):
        m = re.match(r"(?:py.*-)?([\d\.]+)(?:-(\w+))?", vers)
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
            version.append(l & 0xFF)
            l >>= 8
        version.reverse()
        return tuple(version)
