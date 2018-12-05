# File: setup.py
# Date: 6-Oct-2018
#
# Update:
#
import re
import glob

from setuptools import find_packages
from setuptools import setup

packages = []
thisPackage = 'wwpdb.apps.content_ws_server'

with open('wwpdb/apps/content_ws_server/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


setup(
    name=thisPackage,
    version=version,
    description='wwPDB remote Content WS server',
    long_description="See:  README.md",
    author='Ezra Peisach',
    author_email='ezra.peisach@rcsb.org',
    url='https://github.com/rcsb/py-wwpdb_apps_content_ws_server',
    #
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
#        'console_scripts': ['ValidationServiceHandler=wwpdb.apps.val_ws_server.service.ValidationServiceHandler:main']
    },
    #
    # For now, include validation package. Later on may separate web code from backend
    install_requires=['wwpdb.io', 'wwpdb.utils.config', 'wwpdb.utils.db', 'wwpdb.utils.detach',
                      'wwpdb.utils.message_queue', 'wwpdb.utils.ws_utils',
                      'onedep-biocuration-api'],
    packages=find_packages(exclude=['wwpdb.apps.tests-contentws',
                                    'mock-data']),
    # Enables Manifest to be used
    #include_package_data = True,
    package_data={
        # If any package contains *.md or *.rst ...  files, include them:
        '': ['*.md', '*.rst', "*.txt", "*.cfg"],
    },
    #
    # These basic tests require no database services -
    test_suite="wwpdb.apps.tests-contentws",
    tests_require=['tox'],
    #
    # Not configured ...
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    # Added for
    command_options={
        'build_sphinx': {
            'project': ('setup.py', thisPackage),
            'version': ('setup.py', version),
            'release': ('setup.py', version)
        }
    },
    # This setting for namespace package support -
    zip_safe=False,
)
