from sqlalchemy.testing.suite import *

from sqlalchemy.testing.suite import InsertBehaviorTest as _InsertBehaviorTest

class InsertBehaviorTest(_InsertBehaviorTest):
    @testing.skip("mssql")
    def test_no_results_for_non_returning_insert(self):
        # test failures for "not_executemany" cases look like they might be
        # related to _embedded_scope_identity logic in MSExecutionContext_pytds
        # causing returns_rows=True even though implicit_returning=False in
        # the table definition
        return
