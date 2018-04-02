#!/usr/bin/env vpython2
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

class Main(object):
    def __init__(self):
        self.engine = sa.create_engine('mssql+pytds://sa:Admin1!1@127.0.0.1/testing', echo=True)
        print dir(self.engine)
        self.metadata = sa.MetaData(self.engine)

    def close(self):
        pass

    def convert(self, c, row):
        return c.process_rows([row])[0]

    def demo0(self):
        t = sa.Table('#t', self.metadata,
            sa.Column('idrow', sa.Integer, primary_key=True),
            sa.Column('data', sa.String(50)),
        )
        t.create(self.engine)
        with self.engine.begin() as conn:
            for i in range(10):
                result = conn.execute(t.insert(), dict(data="row=%03d"%(i+1)))
        with self.engine.begin() as conn:
            stmt = sa.select(
                t.c
            ).where(
                t.c.idrow < 5
            ).order_by(
                t.c.idrow
            ).execution_options(stream_results=True)
            c = conn.execute(stmt)
            sc = c.cursor
            print 'from last'
            sc.movelast()
            while True:
                rs = sc.fetchone()
                print self.convert(c, rs)
                if not sc.moveprev():
                    break
            print 'from first'
            sc.movefirst()
            while True:
                rs = sc.fetchone()
                print self.convert(c, rs)
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
