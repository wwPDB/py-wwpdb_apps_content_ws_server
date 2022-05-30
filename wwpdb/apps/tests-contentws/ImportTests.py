##
# File: ImportTests.py
# Date:  06-Oct-2018  E. Peisach
#
# Updates:
##
"""Test cases for contentws module"""

import platform

import os
import unittest

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TESTOUTPUT = os.path.join(HERE, "test-output", platform.python_version())
if not os.path.exists(TESTOUTPUT):
    os.makedirs(TESTOUTPUT)
mockTopPath = os.path.join(TOPDIR, "wwpdb", "mock-data")
rwMockTopPath = os.path.join(TESTOUTPUT)

# Must create config file before importing ConfigInfo
from wwpdb.utils.testing.SiteConfigSetup import SiteConfigSetup  # noqa: E402
from wwpdb.utils.testing.CreateRWTree import CreateRWTree  # noqa: E402

# Copy site-config and selected items
crw = CreateRWTree(mockTopPath, TESTOUTPUT)
crw.createtree(["site-config", "wsresources"])
# Use populate r/w site-config using top mock site-config
SiteConfigSetup().setupEnvironment(rwMockTopPath, rwMockTopPath)

from wwpdb.apps.content_ws_server.content.ContentRequest import ContentRequest  # noqa: E402
from wwpdb.apps.content_ws_server.register.Register import Register  # noqa: E402


class ImportTests(unittest.TestCase):
    def setUp(self):
        pass

    def testInstantiate(self):
        """Tests simple instantiation"""
        #        WebServiceApp()
        ContentRequest()
        Register()


if __name__ == "__main__":
    unittest.main()
