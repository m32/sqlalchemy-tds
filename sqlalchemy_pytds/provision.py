from sqlalchemy.testing.provision import normalize_sequence

@normalize_sequence.for_db("mssql")
def normalize_sequence(cfg, sequence):
    # avoid numeric overflow (int) in tests
    if sequence.start is None:
        sequence.start = 1
    return sequence
