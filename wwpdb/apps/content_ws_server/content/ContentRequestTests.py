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


import unittest
import time
import logging

from wwpdb.apps.content_ws_server.content.ContentRequestReport import ContentRequestReport

logger = logging.getLogger()


class ContentRequestReportTests(unittest.TestCase):

    def setUp(self):
        self.__verbose = True
        self.__pdbxFilePath = "../tests/1kip.cif"
        self.__logFilePath = "my.log"
        self.__contentType = 'req-sasbdb-status-report'

    def tearDown(self):
        pass

    def testEntryReport(self):
        """Test case -  report type status
        """
        startTime = time.clock()
        logger.info("Starting")

        try:
            cr = ContentRequestReport(self.__verbose)
            rD = cr.extractContent(self.__pdbxFilePath, self.__logFilePath, self.__contentType)
            logger.info("Extracted %r" % rD)
        except:
            logger.exception("Failing test")
            self.fail()

        endTime = time.clock()
        logger.info("Completed ad (%.2f seconds)\n" % (endTime - startTime))


def suiteEntryReport():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ContentRequestReportTests("testEntryReport"))
    return suiteSelect


if __name__ == '__main__':
    #
    if (True):
        mySuite = suiteEntryReport()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

