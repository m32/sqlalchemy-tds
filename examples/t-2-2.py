import pytds

from tconfig import username, userpass


class Main(object):
    def __init__(self):
        self.conn = pytds.connect(
            dsn="127.0.0.1", user=username, password=userpass, database="testing"
        )

    def close(self):
        self.conn.close()

    def bug(self):
        sqls = (
            "create table #sqlvariant_test(val_type varchar(20) primary key, val sql_variant)",
        )
        c = self.conn.cursor()
        for sql in sqls:
            c.execute(sql)
        c.close()

        sqls = (
            ("INSERT INTO #sqlvariant_test values( %s, %s)", "integer", 1),
            ("INSERT INTO #sqlvariant_test values( %s, %s)", "float", 1.1),
            (
                "INSERT INTO #sqlvariant_test values( %s, %s)",
                "decimal(8,2)",
                "CAST(1.1 as decimal(8,2))",
            ),
            ("INSERT INTO #sqlvariant_test values( %s, %s)", "string", "string"),
            ("INSERT INTO #sqlvariant_test values( %s, %s)", "string", b"bytes"),
            ("COMMIT",),
        )
        c = self.conn.cursor()
        for sqlp in sqls:
            sql = sqlp[0]
            params = sqlp[1:]
            c.execute(sql, params)
        c.close()

        sqls = ("SELECT * FROM #sqlvariant_test",)
        c = self.conn.cursor()
        for sql in sqls:
            c.execute(sql)
            for r in c.fetchall():
                print(r)
        c.close()

    def main(self):
        self.bug()


def main():
    cls = Main()
    try:
        cls.main()
    finally:
        cls.close()


main()
