#!/usr/bin/env vpython3
from t import username, userpass
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
            sa.Column("idrow", sa.Integer, primary_key=True),
            sa.Column("data", sa.String(50)),
        )
        t.create(self.engine)
        with self.engine.begin() as conn:
            result = conn.execute(t.insert(), dict(data="some % value"))
            print("pk 1=", result.inserted_primary_key[0])
            result = conn.execute(t.insert(), dict(data="some %% value"))
            print("pk 2=", result.inserted_primary_key[0])

            c = conn.execute(t.select())
            for rs in c.fetchall():
                print(rs)

            print(
                conn.scalar(
                    t.select()
                    .where(t.c.data == "some % value")
                    .with_only_columns(t.c.data)
                ),
                "=" * 10,
                "some % value",
            )

            print(
                conn.scalar(
                    t.select()
                    .where(t.c.data == "some %% value")
                    .with_only_columns(t.c.data)
                ),
                "=" * 10,
                "some %% value",
            )

    def main(self):
        self.bug1()


def main():
    cls = Main()
    try:
        cls.main()
    finally:
        cls.close()


main()
