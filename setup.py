import sys
import os
import re

if sys.version_info < (2, 6):
    raise Exception("SQLAlchemy TDS requires Python 2.6 or higher.")

from setuptools import setup

v = open(os.path.join(os.path.dirname(__file__), 'sqlalchemy_pytds', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
requires = [
    'python-tds',
    'SQLAlchemy',
]

setup(name='sqlalchemy_pytds',
      version=VERSION,
      description="A Microsoft SQL Server TDS connector for SQLAlchemy.",
      long_description=open(readme).read(),
      long_description_content_type='text/x-rst',
      author='Grzegorz Makarewicz',
      author_email='mak@trisoft.com.pl',
      url='https://github.com/m32/sqlalchemy-tds',
      license='MIT',
      platforms=["any"],
      packages=['sqlalchemy_pytds'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Database :: Front-Ends',
      ],
      keywords='SQLAlchemy Microsoft SQL Server',
      install_requires = requires,
      include_package_data=True,
      tests_require=['nose >= 0.11'],
      test_suite="nose.collector",
      entry_points={
         'sqlalchemy.dialects': [
              'mssql.pytds = sqlalchemy_pytds.dialect:MSDialect_pytds',
              ]
        }
)
