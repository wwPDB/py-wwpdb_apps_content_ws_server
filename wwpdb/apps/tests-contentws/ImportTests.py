##
# File: ImportTests.py
# Date:  06-Oct-2018  E. Peisach
#
# Updates:
##
"""Test cases for contentws module"""

import os
import sys
import unittest

if __package__ is None or __package__ == "":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from commonsetup import HERE  # noqa:  F401 pylint: disable=import-error,unused-import
else:
    from .commonsetup import HERE  # noqa: F401 pylint: disable=relative-beyond-top-level

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
