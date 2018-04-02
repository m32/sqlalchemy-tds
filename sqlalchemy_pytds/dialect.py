from sqlalchemy.dialects.mssql.base import MSDialect, MSExecutionContext
from .connector import PyTDSConnector


class MSExecutionContext_pytds(MSExecutionContext):
    _embedded_scope_identity = False

    def pre_exec(self):
        super(MSExecutionContext_pytds, self).pre_exec()
        if self._select_lastrowid and \
                self.dialect.use_scope_identity and \
                len(self.parameters[0]):
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

class MSDialect_pytds(PyTDSConnector, MSDialect):

    execution_ctx_cls = MSExecutionContext_pytds

    def __init__(self, **params):
        super(MSDialect_pytds, self).__init__(**params)
        self.use_scope_identity = True

    def set_isolation_level(self, connection, level):
        if level == 'AUTOCOMMIT':
            connection.autocommit(True)
        else:
            connection.autocommit(False)
            super(MSDialect_pytds, self).set_isolation_level(connection,
                                                               level)
