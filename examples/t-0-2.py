#!/usr/bin/env vpython3
from t import username, userpass
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

class Main(object):
    def __init__(self):
        self.engine = sa.create_engine('mssql+pytds://'+username+':'+userpass.replace('@', '%40')+'@127.0.0.1/testing')
        self.metadata = sa.MetaData()

    def close(self):
        pass

    def bug1(self):
        print('*'*20, 'bug 0')
        t = sa.Table('#t', self.metadata,
            sa.Column('idrow', sa.Integer, primary_key=True),
            sa.Column('data', sa.String(50)),
        )
        t.create(self.engine)

        Session = sessionmaker(bind=self.engine)
        session = Session()

        stmt = t.delete()
        result = session.execute(stmt)
        session.commit()

        stmt = t.insert().values(data="some % value")
        result = session.execute(stmt)
        print('pk 1', result.inserted_primary_key[0])
        stmt = t.insert().values(data="some %% value")
        result = session.execute(stmt)
        print('pk 2', result.inserted_primary_key[0])
        session.commit()

        print('*'*20, 'all')
        c = session.execute(
            t.select()
        )
        for rs in c.fetchall():
            print(rs)

        if 1:
            print('*'*20, 'literal column', 'some % value')
            print(
                session.scalar(
                    t.select(
                    ).where(
                        t.c.data == sa.literal_column("'some % value'")
                    ).with_only_columns(
                        t.c.data
                    )
                ),
                '='*10,
                "some % value"
            )
        if 1:
            print('*'*20, 'literal column', 'some %% value')
            print(
                session.scalar(
                    t.select(
                    ).where(
                        t.c.data == sa.literal_column("'some %% value'")
                    ).with_only_columns(
                        t.c.data
                    )
                ),
                '='*10,
                "some %% value"
            )
        if 1:
            print('*'*20, 'variable')
            v = "some %% value"
            print(
                session.scalar(
                    t.select(
                    ).where(
                        t.c.data == v
                    ).with_only_columns(
                        t.c.data
                    )
                ),
                '='*10,
                v
            )

        session.rollback()

    def main(self):
        self.bug1()

def main():
    cls = Main()
    try:
        cls.main()
    finally:
        cls.close()
main()
