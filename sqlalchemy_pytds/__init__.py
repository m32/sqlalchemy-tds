__version__ = "1.0.2"

from sqlalchemy.dialects import registry

registry.register("mssql.pytds", "sqlalchemy_pytds.dialect", "MSDialect_pytds")
