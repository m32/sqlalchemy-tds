#!/usr/bin/env vpython2
import os
import pytds

class Main(object):
    def __init__(self):
        self.conn = pytds.connect(dsn='127.0.0.1', user='sa', password='Admin1!1', database='master', autocommit=True)

    def close(self):
        self.conn.close()

    def main(self):
        cwd = os.getcwd()
        sqls = (
            '''\
DROP DATABASE IF EXISTS testing;
''',
            '''\
CREATE DATABASE testing ON (
    NAME = testing_dat,
    FILENAME = '%(cwd)s/testing_mdf.mdf',
    SIZE = 10,
    FILEGROWTH = 5
) LOG ON (
    NAME = testing_log,
    FILENAME = '%(cwd)s/testing_ldf.ldf',
    SIZE = 5MB,
    FILEGROWTH = 5MB
)
''' % {'cwd':cwd},
            '''\
USE testing
''',
            '''\
DROP SCHEMA IF EXISTS test_schema
''',
            '''\
CREATE SCHEMA test_schema;
''',
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
