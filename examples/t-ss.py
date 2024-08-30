#!/usr/bin/env vpython3
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from tconfig import username, userpass


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

    def demo0(self):
        t = sa.Table(
            "#t",
            self.metadata,
            sa.Column("idrow", sa.Integer, primary_key=True),
            sa.Column("data", sa.String(50)),
        )
        t.create(self.engine)
        with self.engine.begin() as conn:
            for i in range(10):
                result = conn.execute(t.insert(), dict(data="row=%03d" % (i + 1)))
        with self.engine.begin() as conn:
            stmt = (
                sa.select(t.c)
                .where(t.c.idrow < 5)
                .order_by(t.c.idrow)
                .execution_options(stream_results=True)
            )
            c = conn.execute(stmt)
            sc = c.cursor
            print("from last")
            sc.movelast()
            while True:
                rs = sc.fetchone()
                print(rs)
                if not sc.moveprev():
                    break
            print("from first")
            sc.movefirst()
            while True:
                rs = sc.fetchone()
                print(rs)
                if not sc.movenext():
                    break
            c.close()

    def main(self):
        self.demo0()


def main():
    cls = Main()
    try:
        cls.main()
    finally:
        cls.close()


main()
