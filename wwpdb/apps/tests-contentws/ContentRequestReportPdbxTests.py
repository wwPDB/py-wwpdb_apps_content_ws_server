##
#
# File:    ContentRequestReportPdbxTests.py
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

import json
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

FORMAT = "[%(levelname)s]-%(module)s.%(funcName)s: %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class ContentRequestReportPdbxTests(unittest.TestCase):
    def setUp(self):
        self.__verbose = True
        self.__pdbxFilePath = os.path.join(HERE, "data", "1kip.cif")
        self.__logFilePath = "my.log"

    def tearDown(self):
        pass

    def testEntryReader(self):
        """Test case -  report type status"""
        startTime = time.time()
        logger.info("Starting")

        try:
            cr = ContentRequestReportPdbx(self.__verbose)
            rD = cr.readFilePdbx(self.__pdbxFilePath, self.__logFilePath, ["entity", "entity_poly", "database_2"])
            logger.info("Data file content %r", rD)
        except:  # noqa: E722 pylint: disable=bare-except
            logger.exception("Failing test")
            self.fail()

        endTime = time.time()
        logger.info("Completed ad (%.2f seconds)", endTime - startTime)

    def testContentTypeReader(self):
        """Test case -  report type status"""
        startTime = time.time()
        logger.info("Starting")

        try:
            cr = ContentRequestReportPdbx(self.__verbose)
            rL = cr.getContentTypes()
            logger.info("Content type definitions %r", rL)
        except:  # noqa: E722 pylint: disable=bare-except
            logger.exception("Failing test")
            self.fail()

        endTime = time.time()
        logger.info("Completed ad (%.2f seconds)", endTime - startTime)

    def testEntryReport(self):
        """Test case -  report type status"""
        startTime = time.time()
        logger.info("Starting")

        try:
            cr = ContentRequestReportPdbx(self.__verbose)
            ctypeL = cr.getContentTypes()
            self.assertNotEqual(ctypeL, [], "Could not parse content types")
            for ctype in ctypeL:
                if ctype.startswith("report-entry-"):
                    logger.info("Definition %r", ctype)
                    rD = cr.extractContent(self.__pdbxFilePath, self.__logFilePath, ctype)
                    logger.info("File content %r", rD)
                    # 1kip has three entity_poly
                    self.assertEqual(len(rD["entity_poly"]), 3)
                    ss = json.dumps(rD)
                    logger.info("JSON serialized result %r", ss)
        except:  # noqa: E722 pylint: disable=bare-except
            logger.exception("Failing test")
            self.fail()

        endTime = time.time()
        logger.info("Completed ad (%.2f seconds)", endTime - startTime)


def suiteEntryReport():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ContentRequestReportPdbxTests("testEntryReader"))
    suiteSelect.addTest(ContentRequestReportPdbxTests("testContentTypeReader"))
    suiteSelect.addTest(ContentRequestReportPdbxTests("testEntryReport"))
    return suiteSelect


if __name__ == "__main__":
    #
    mySuite = suiteEntryReport()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
