from t import username, userpass
import pytds

conn = pytds.connect(dsn='127.0.0.1', user=username, password=userpass, database='testing')
def sqlexec(sql, params, fetch=False):
    c = conn.cursor()
    c.execute(sql, params)
    if fetch:
        for r in c.fetchall():
            print(r)
    c.close()
try:
    sqlexec('create table #sqlvariant_test(val_type varchar(20) primary key, val sql_variant)',())
    sqlexec("INSERT INTO #sqlvariant_test values( %s, %s)", ('integer', 1))
    sqlexec("INSERT INTO #sqlvariant_test values( %s, %s)", ('float', 1.1))
    sqlexec("INSERT INTO #sqlvariant_test values( %s, %s)", ('decimal(8,2)', 'CAST(1.1 as decimal(8,2))'))
    sqlexec("INSERT INTO #sqlvariant_test values( %s, %s)", ('string', 'string'))
    sqlexec("INSERT INTO #sqlvariant_test values( %s, %s)", ('bytes', b'bytes'))
    sqlexec("COMMIT", ())
    sqlexec("SELECT * FROM #sqlvariant_test", (), True)
finally:
    conn.close()