import sys
import os
import re

cmdclass = {}
if sys.version_info < (2, 6):
    raise Exception("SQLAlchemy TDS requires Python 2.6 or higher.")

from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    # from https://pytest.org/latest/goodpractises.html\
    # #integration-with-setuptools-test-commands
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    default_options = ["-n", "4", "-q"]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(
            " ".join(self.default_options) + " " + self.pytest_args)
        sys.exit(errno)

cmdclass['test'] = PyTest

v = open(os.path.join(os.path.dirname(__file__), 'sqlalchemy_pytds', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()

readme = os.path.join(os.path.dirname(__file__), 'README.rst')


setup(name='sqlalchemy_pytds',
      version=VERSION,
      description="MS SQL Server for SQLAlchemy",
      long_description=open(readme).read(),
      classifiers=[
      'Development Status :: 3 - Alpha',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: Implementation :: CPython',
      'Topic :: Database :: Front-Ends',
      ],
      keywords='SQLAlchemy Microsoft SQL Server',
      author='Grzegorz Makarewicz',
      author_email='mak@trisoft.com.pl',
      license='MIT',
      packages=['sqlalchemy_pytds'],
      include_package_data=True,
      cmdclass=cmdclass,
      zip_safe=False,
      entry_points={
         'sqlalchemy.dialects': [
              'mssql.pytds = sqlalchemy_pytds.dialect:MSDialect_pytds',
              ]
        }
)
