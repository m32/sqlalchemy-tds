#!/usr/bin/env vpython3
import pytds

from t import username, userpass


class Main(object):
    def __init__(self):
        self.conn = pytds.connect(
            dsn="127.0.0.1",
            user=username,
            password=userpass,
            database="master",
            autocommit=True,
        )

    def close(self):
        self.conn.close()

    def main(self):
        sqls = (
            """\
DROP DATABASE IF EXISTS testing;
""",
            """\
CREATE DATABASE testing ON (
    NAME = testing_dat,
    FILENAME = '/var/opt/mssql/data/testing_mdf.mdf',
    SIZE = 10,
    FILEGROWTH = 5
) LOG ON (
    NAME = testing_log,
    FILENAME = '/var/opt/mssql/data/testing_ldf.ldf',
    SIZE = 5MB,
    FILEGROWTH = 5MB
)
""",
            """\
USE testing
""",
            """\
DROP SCHEMA IF EXISTS test_schema
""",
            """\
CREATE SCHEMA test_schema;
""",
        )
        c = self.conn.cursor()
        for sql in sqls:
            c.execute(sql)
        c.close()


def main():
    cls = Main()
    try:
        cls.main()
    finally:
        cls.close()


main()
