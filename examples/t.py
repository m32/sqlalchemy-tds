import sys
sys.path.insert(1, '..')
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("sqlalchemy").setLevel(logging.DEBUG)
# logging.getLogger('pytds').setLevel(logging.DEBUG)
# logging.getLogger('pytds.__init__').setLevel(logging.DEBUG)
# logging.getLogger('pytds.tds').setLevel(logging.DEBUG)

username = "sa"
userpass = "SaAdmin1@"
