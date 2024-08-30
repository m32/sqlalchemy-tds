import datetime
from decimal import Decimal

from sqlalchemy import Column, Table, insert, select, testing
from sqlalchemy.dialects.mssql import SQL_VARIANT
from sqlalchemy.exc import OperationalError
from sqlalchemy.testing import eq_, fixtures


class SqlVariantTest(fixtures.TablesTest):
    run_create_tables = "each"
    __backend__ = True

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "sql_variant_test",
            metadata,
            Column("sql_variant_col", SQL_VARIANT),
        )

    @testing.combinations(
        ("datetime2", datetime.datetime(2021, 2, 3, 4, 5, 6, 7000), False),
        (
            "datetimeoffset",
            datetime.datetime(2021, 2, 3, 4, 5, 6, 7000, tzinfo=datetime.timezone.utc),
            False,
        ),
        ("py_bytes", b"\xab\xcd", False),
        ("py_bytes_max_len", b"\xab" * 7999, False),
        ("py_decimal", Decimal("1.414"), False),
        ("py_float", 3.14, False),
        ("py_int", 123, False),
        ("py_none", None, False),
        ("py_string", "Hello World!", False),
        ("py_string_max_len", "x" * 4000, False),
        ("py_string_too_long", "x" * 4001, True),
        argnames="variant_value,expect_error",
        id_="iaa",
    )
    def test_sql_variant_roundtrip(self, connection, variant_value, expect_error):
        tbl = self.tables.sql_variant_test
        try:
            connection.execute(
                insert(tbl),
                dict(sql_variant_col=variant_value),
            )
            if expect_error:
                raise Exception("Expected error did not occur.")
            fetched_value = connection.execute(select(tbl.c.sql_variant_col)).scalar()
            eq_(fetched_value, variant_value)
        except OperationalError as oe:
            if not expect_error:
                raise
