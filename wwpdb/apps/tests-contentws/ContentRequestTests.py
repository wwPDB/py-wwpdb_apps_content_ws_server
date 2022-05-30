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

import platform

import logging
import os
import time
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
