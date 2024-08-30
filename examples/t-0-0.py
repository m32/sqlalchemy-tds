#!/usr/bin/env vpython3
from t import username, userpass
import pytds


class Main(object):
    def __init__(self):
        self.conn = pytds.connect(
            dsn="127.0.0.1", user=username, password=userpass, database="testing"
        )

    def close(self):
        self.conn.close()

    def bug1(self):
        print("*" * 20, "bug 0")
        sqls = (
            "create table #t(idrow int identity(1, 1) primary key,data varchar(50))",
        )
        c = self.conn.cursor()
        for sql in sqls:
            c.execute(sql)
        c.close()
        # self.conn.commit()

        sql = "INSERT INTO #t (data) VALUES (%(data)s)"
        c = self.conn.cursor()
        c.execute(sql, {"data": "some % value"})
        c.execute(sql, {"data": "some %% value"})
        c.close()
        # self.conn.commit()

        sqls = (
            """SELECT data FROM #t""",
            """SELECT data FROM #t WHERE data = 'some % value' """,
            """SELECT data FROM #t WHERE data = 'some %% value' """,
        )
        c = self.conn.cursor()
        for sql in sqls:
            print("*" * 20)
            print(sql)
            c.execute(sql)
            for rs in c.fetchall():
                print(rs)
        c.close()

    def main(self):
        self.bug1()


def main():
    cls = Main()
    try:
        cls.main()
    finally:
        cls.close()


main()
