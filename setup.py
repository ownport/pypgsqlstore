
import os
import sys
from codecs import open

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), 'r', 'utf-8') as handle:
    readme = handle.read()


def build_package_names(path):

    packages = [path, ]
    for root, dirs, files in os.walk(path):
        packages.extend(['.'.join([root, d]) for d in dirs])
    return packages


setup(
    name = 'pypgsqlstore',
    version = '0.1.0.dev0',
    description = "Store documents in PgSQL database",
    long_description = readme,
    # long_description_content_type = 'text/markdown',
    packages=build_package_names('pypgsqlstore'),
    python_requires = '>=3.5',
    entry_points = {
        'console_scripts': [ 
            'pypgsqlstore=pypgsqlstore.cli:launch_new_instance', 
        ]
    }
)
