Testing is done using pytest. After installing pytest via ``pip``, a typical run of the SQLAlchemy test suite
can be performed by running:
   python3 -m pytest
for more verbose output:
   python3 -m pytest -v
or:
   python3 -m pytest --log-debug=pytds --log-debug=sqlalchemy.engine

results with SQLAlchemy==2.0.34, python-tds==1.15.0
================= 768 passed, 788 skipped, 1 warning in 56.72s =================

IMPORTANT:

1. Couple of tests require the testing database to contain a User-defined Schema named ``test_schema``
   Create it before running test with:
      python3 createdb.py
