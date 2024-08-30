from t import username, userpass
import decimal
from sqlalchemy import Column, String, create_engine, select, update
from sqlalchemy.dialects.mssql import SQL_VARIANT
from sqlalchemy.orm import Session, declarative_base

engine = create_engine('mssql+pytds://'+username+':'+userpass.replace('@', '%40')+'@127.0.0.1/testing')
Base = declarative_base()

class Thing(Base):
    __tablename__ = "#sqlvariant_test"
    val_type = Column(String(20), primary_key=True)
    val = Column(SQL_VARIANT, nullable=True)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(engine) as sess:
    sess.add(Thing(val_type="py_int", val=1))
    sess.add(Thing(val_type="py_decimal", val=decimal.Decimal('1.1')))
    sess.add(Thing(val_type="py_float", val=1.2))
    # WTF TODO
    # after uncommenting the line below everything is ok
    sess.commit()
    sess.add(Thing(val_type="py_string", val="Hello World!"))
    sess.commit()
    sess.add(Thing(val_type="py_bytes", val=b"Hello World!"))
    sess.add(Thing(val_type="py_none", val=None))
    for i in range(20):
        sess.add(Thing(val_type=f"py_bytes{i}", val=b"Hello World!"))
    sess.commit()

    stmt = select(Thing.val_type, Thing.val).order_by(Thing.val_type)
    rows = sess.execute(stmt).fetchall()
    for row in rows:
        print(row)
    sess.commit()

    #stmt = update(Thing).values(val=b'ala ma kota').where(Thing.val_type=='py_bytes')
    stmt = update(Thing).values(val=b'\xab\xcd'*4000).where(Thing.val_type=='py_bytes')
    stmt = update(Thing).values(val='a'*4000).where(Thing.val_type=='py_string')
    #print('stmt', str(stmt))
    sess.execute(stmt)
    sess.commit()

    stmt = select(Thing.val_type, Thing.val).order_by(Thing.val_type)
    rows = sess.execute(stmt).fetchall()
    for row in rows:
        print(row)
    sess.commit()
