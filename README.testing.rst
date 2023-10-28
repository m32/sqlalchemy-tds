Testing is done using pytest. After installing pytest via ``pip``, a typical run of the SQLAlchemy test suite
can be performed by running::

python3 -m pytest
or, for more verbose output::
python3 -m pytest -v
or:
python3 -m pytest --log-info=sqlalchemy.engine --log-debug=pytds --log-debug=sqlalchemy.engine

results:
64 failed
686 passed
767 skipped
1 warning

IMPORTANT:

1. Couple of tests require the testing database to contain a User-defined Schema named ``test_schema``
   Create it before running test with python3 createdb.py
