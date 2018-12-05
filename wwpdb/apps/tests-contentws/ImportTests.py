##
# File: ImportTests.py
# Date:  06-Oct-2018  E. Peisach
#
# Updates:
##
"""Test cases for contentws module"""

import unittest

from wwpdb.apps.content_ws_server.webapp.WebServiceApp import WebServiceApp
from wwpdb.apps.content_ws_server.content.ContentRequest import ContentRequest


class ImportTests(unittest.TestCase):
    def setUp(self):
        pass

    def testInstantiate(self):
        """Tests simple instantiation"""
#        WebServiceApp()
        ContentRequest()
        pass


if __name__ == '__main__':
    unittest.main()
