##
#
# File:    ContentRequestTests.py
# Author:  J. Westbrook
# Date:    12-Feb-2017
# Version: 0.001
#
# Updates:
#
##
"""
Test cases for extracting content from PDBx format files and building
reports -

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import logging
import os
import time
import sys
import unittest

if __package__ is None or __package__ == "":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from commonsetup import HERE  # noqa:  F401 pylint: disable=import-error,unused-import
else:
    from .commonsetup import HERE  # noqa: F401 pylint: disable=relative-beyond-top-level

from wwpdb.apps.content_ws_server.content.ContentRequestReportPdbx import ContentRequestReportPdbx  # noqa: E402

logger = logging.getLogger()
ch = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


@unittest.skip("Tests need to be ported. Might no longer be relevant")
class ContentRequestReportTests(unittest.TestCase):
    def setUp(self):
        self.__verbose = True
        self.__pdbxFilePath = "../tests/1kip.cif"
        self.__logFilePath = "my.log"
        self.__contentType = "req-sasbdb-status-report"

    def tearDown(self):
        pass

    def testEntryReport(self):
        """Test case -  report type status"""
        startTime = time.time()
        logger.info("Starting")

        try:
            cr = ContentRequestReportPdbx(self.__verbose)
            rD = cr.extractContent(self.__pdbxFilePath, self.__logFilePath, self.__contentType)
            logger.info("Extracted %r", rD)
        except:  # noqa: E722 pylint: disable=bare-except
            logger.exception("Failing test")
            self.fail()

        endTime = time.time()
        logger.info("Completed ad (%.2f seconds)", endTime - startTime)


def suiteEntryReport():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ContentRequestReportTests("testEntryReport"))
    return suiteSelect


if __name__ == "__main__":
    #
    mySuite = suiteEntryReport()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
