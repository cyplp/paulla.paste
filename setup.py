# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'pyramid_fanstatic',
    'rebecca.fanstatic',
    'couchdbkit',
    'pyramid_beaker',
    'Pygments',
    'Babel',
    'lingua',
    'py-bcrypt',
    'pyramid_xmlrpc',
    ]

setup(name='paulla.paste',
      version='0.0',
      description='paulla.paste',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author=u'Cyprien Le Pannérer',
      author_email='cyplp@free.fr',
      url='',
      keywords='paste couchdb pyramid',
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['paulla'],
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="paullapaste",
      entry_points = """\
      [paste.app_factory]
      main = paulla.paste:main
      """,
      message_extractors = { "paulla":
                             [
             ('**.py',   'lingua_python', None ),
             ('**.pt',   'lingua_xml', None ),

            ]},
      )

