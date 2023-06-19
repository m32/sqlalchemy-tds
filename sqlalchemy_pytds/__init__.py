__version__ = '0.4.0'

from sqlalchemy.dialects import registry

registry.register("mssql.pytds", "sqlalchemy_pytds.dialect", "MSDialect_pytds")
