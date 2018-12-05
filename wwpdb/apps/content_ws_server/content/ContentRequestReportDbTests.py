##
#
# File:    ContentRequestReportDbTests.py
# Author:  J. Westbrook
# Date:    12-Feb-2017
# Version: 0.001
#
# Updates:
#
##
"""
Test cases for extracting content from rdbms database services and building
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
import json

from wwpdb.api.facade.ConfigInfo import getSiteId
from wwpdb.apps.content_ws_server.content.ContentRequestReportDb import ContentRequestReportDb

FORMAT = '[%(levelname)s]-%(module)s.%(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class ContentRequestReportDbTests(unittest.TestCase):

    def setUp(self):
        self.__verbose = True
        self.__contentTypeList = ['req-emdb-summary-admin-report', 'req-emdb-summary-status-report']
        self.__siteId = getSiteId(defaultSiteId=None)

    def tearDown(self):
        pass

    def testContentTypeReader(self):
        """Test case -  read summary report content type
        """
        startTime = time.clock()
        logger.info("Starting")

        try:
            for ct in self.__contentTypeList:
                cr = ContentRequestReportDb(siteId=self.__siteId, verbose=self.__verbose)
                rL = cr.getContentTypes()
                logger.info("Content type definitions %r" % rL)
        except:
            logger.exception("Failing test")
            self.fail()

        endTime = time.clock()
        logger.info("Completed ad (%.2f seconds)\n" % (endTime - startTime))

    def testSummaryReport(self):
        """Test case -  create summary report
        """
        startTime = time.clock()
        logger.info("Starting")

        try:
            cr = ContentRequestReportDb(siteId=self.__siteId, verbose=self.__verbose)
            ctL = cr.getContentTypes()
            for ct in ctL:
                if ct.startswith("report-summary-"):
                    cD = cr.getContentTypeDef(ct)
                    logger.info("Content definition %r" % cD)
                    rD = cr.extractContent(ct)
                    logger.info("Database content length %r" % len(rD))
                    ss = json.dumps(rD)
                    logger.info("JSON serialized result length %r" % len(ss))
        except:
            logger.exception("Failing test")
            self.fail()

        endTime = time.clock()
        logger.info("Completed ad (%.2f seconds)\n" % (endTime - startTime))


def suiteSummaryReport():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ContentRequestReportDbTests("testContentTypeReader"))
    suiteSelect.addTest(ContentRequestReportDbTests("testSummaryReport"))
    return suiteSelect


if __name__ == '__main__':
    #
    if (True):
        mySuite = suiteSummaryReport()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
