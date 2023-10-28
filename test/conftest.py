from sqlalchemy.dialects import registry
import pytest

registry.register("mssql.pytds", "sqlalchemy_pytds.dialect", "MSDialect_pytds")

pytest.register_assert_rewrite("sqlalchemy.testing.assertions")

from sqlalchemy.testing.plugin.pytestplugin import *
