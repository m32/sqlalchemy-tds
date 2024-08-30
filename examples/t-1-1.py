#!/usr/bin/env vpython3
from t import username, userpass
import decimal
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker


class Main(object):
    def __init__(self):
        self.engine = sa.create_engine(
            "mssql+pytds://"
            + username
            + ":"
            + userpass.replace("@", "%40")
            + "@127.0.0.1/testing"
        )
        self.metadata = sa.MetaData()

    def close(self):
        pass

    def bug1(self):
        print("*" * 20, "bug 0")
        t = sa.Table(
            "#t",
            self.metadata,
            sa.Column(
                "data", sa.Float(precision=8, decimal_return_scale=4, asdecimal=True)
            ),
        )
        t.create(self.engine)
        with self.engine.begin() as conn:
            conn.execute(t.insert(), dict(data=15.7563))
            conn.execute(t.insert(), dict(data=decimal.Decimal("15.7563")))
            c = conn.execute(t.select())
            for rs in c.fetchall():
                print(rs)

    def main(self):
        self.bug1()


def main():
    cls = Main()
    try:
        cls.main()
    finally:
        cls.close()


main()
