import re

from pytds import tds_base, tds_types
from sqlalchemy import util
from sqlalchemy.dialects.mssql import SQL_VARIANT
from sqlalchemy.dialects.mssql.base import (
    MSDialect,
    MSExecutionContext,
    MSIdentifierPreparer,
    MSSQLCompiler,
)
from sqlalchemy.engine.interfaces import ExecuteStyle

from .connector import PyTDSConnector

_server_side_id = util.counter()


class SSCursor(object):
    def __init__(self, c):
        self._c = c
        self._name = None
        self._nrows = 0
        self._row = 0

    def execute(self, statement, parameters):
        _name = "tc%08X" % _server_side_id()
        sql = (
            "DECLARE "
            + _name
            + " CURSOR GLOBAL SCROLL STATIC READ_ONLY FOR "
            + statement
        )
        # print(sql, parameters)
        self._c.execute(sql, parameters)
        self._name = _name
        sql = "OPEN " + _name
        self._c.execute(sql)
        self._c.execute("SELECT @@CURSOR_ROWS AS nrows")
        self._nrows = self._c.fetchone()[0]
        return self.fetchone()

    def close(self):
        sql = "CLOSE " + self._name
        self._c.execute(sql)
        sql = "DEALLOCATE " + self._name
        self._c.execute(sql)
        self._c.close()
        self._name = None
        self._nrows = 0
        self._row = 0

    def fetchone(self):
        if not (0 <= self._row < self._nrows):
            return None
        sql = "FETCH ABSOLUTE %d FROM %s" % (self._row + 1, self._name)
        self._c.execute(sql)
        return self._c.fetchone()

    def movefirst(self):
        value = 0
        if value >= 0 and value < self._nrows:
            self._row = value
            return True
        return False

    def moveprev(self):
        value = self._row - 1
        if value >= 0 and value < self._nrows:
            self._row = value
            return True
        return False

    def movenext(self):
        value = self._row + 1
        if value >= 0 and value < self._nrows:
            self._row = value
            return True
        return False

    def movelast(self):
        value = self._nrows - 1
        if value >= 0 and value < self._nrows:
            self._row = value
            return True
        return False

    def goto(self, value):
        if value >= 0 and value < self._nrows:
            self._row = value
            return True
        return False

    def __getattr__(self, name):
        # print('getattr(%s)' %name)
        return getattr(self._c, name)


class MSSQLCompiler_pytds(MSSQLCompiler):
    pass


class MSSQLIdentifierPreparer_pytds(MSIdentifierPreparer):

    def _escape_identifier(self, value: str) -> str:
        value = value.replace("]", "]]")
        value = value.replace("%", "%%")
        return value

    def _unescape_identifier(self, value: str) -> str:
        return value.replace("]]", "]")


class MSExecutionContext_pytds(MSExecutionContext):
    _embedded_scope_identity = False

    def pre_exec(self):
        super(MSExecutionContext_pytds, self).pre_exec()
        if (
            self._select_lastrowid
            and self.dialect.use_scope_identity
            and len(self.parameters[0])
        ):
            self._embedded_scope_identity = True

            self.statement += "; select scope_identity()"

    def post_exec(self):
        if self._embedded_scope_identity:
            while True:
                try:
                    row = self.cursor.fetchall()[0]
                    break
                except self.dialect.dbapi.Error as e:
                    self.cursor.nextset()

            self._lastrowid = int(row[0])
            self.cursor.lastrowid = int(row[0])
            self._select_lastrowid = False
        super(MSExecutionContext_pytds, self).post_exec()

    def create_cursor(self):
        usess = self.execution_options.get("stream_results", None)
        if usess:
            self._is_server_side = True
            return SSCursor(self._dbapi_connection.cursor())
        else:
            self._is_server_side = False
            return self._dbapi_connection.cursor()


class MSDialect_pytds(PyTDSConnector, MSDialect):

    execution_ctx_cls = MSExecutionContext_pytds
    statement_compiler = MSSQLCompiler_pytds
    preparer = MSSQLIdentifierPreparer_pytds  # type: ignore

    supports_server_side_cursors = True
    supports_statement_cache = True
    supports_sane_rowcount_returning = True
    supports_sane_multi_rowcount = False
    supports_native_decimal = True
    supports_native_uuid = True

    def __init__(self, server_side_cursors=False, **params):
        super(MSDialect_pytds, self).__init__(**params)
        self.use_scope_identity = True
        self.server_side_cursors = server_side_cursors

    def do_execute(self, cursor, statement, parameters, context=None):
        if context and context.isinsert or context.isupdate:
            tbl = context.compiled.compile_state.dml_table
            # print('*'*20, 'do_execute')
            # print('stmt:', statement)
            # print('parm:', parameters)
            for c in tbl._columns:
                if isinstance(c.type, SQL_VARIANT):
                    todo = [
                        name
                        for name in parameters.keys()
                        if c.name == name or re.match(c.name + r"__(\d+)", name)
                    ]
                    # print('todo:', todo)
                    for name in todo:
                        v = parameters.get(name, None)
                        # print('cvt', name, v)
                        if isinstance(v, str):
                            # assert len(v) <= 4000
                            parameters[name] = tds_base.Param(
                                name=name,
                                type=tds_types.NVarCharType(size=len(v)),
                                value=v,
                                flags=0,
                            )
                        elif isinstance(v, bytes):
                            # assert len(v) <= 8000
                            parameters[name] = tds_base.Param(
                                name=name,
                                type=tds_types.VarBinaryType(size=len(v)),
                                value=v,
                                flags=0,
                            )
            # print('parm:', parameters)
        cursor.execute(statement, parameters)

    def set_isolation_level(self, connection, level):
        if level == "AUTOCOMMIT":
            connection.autocommit(True)
        else:
            connection.autocommit(False)
            super(MSDialect_pytds, self).set_isolation_level(connection, level)
