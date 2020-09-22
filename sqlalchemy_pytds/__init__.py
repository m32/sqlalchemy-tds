__version__ = '0.3.1'

from sqlalchemy.dialects import registry

registry.register("mssql.pytds", "sqlalchemy_pytds.dialect", "MSDialect_pytds")
