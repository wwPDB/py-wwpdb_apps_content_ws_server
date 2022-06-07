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

from wwpdb.utils.config.ConfigInfo import getSiteId  # noqa: E402
from wwpdb.apps.content_ws_server.content.ContentRequestReportDb import ContentRequestReportDb  # noqa: E402
from wwpdb.utils.testing.Features import Features  # noqa: E402

FORMAT = "[%(levelname)s]-%(module)s.%(funcName)s: %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@unittest.skipUnless(Features().haveMySqlTestServer(), "Needs test DB environment")
class ContentRequestReportDbTests(unittest.TestCase):
    def setUp(self):
        self.__verbose = True
        self.__siteId = getSiteId(defaultSiteId=None)

    def tearDown(self):
        pass

    def testContentTypeReader(self):
        """Test case -  read summary report content type"""
        startTime = time.time()
        logger.info("Starting")

        try:
            cr = ContentRequestReportDb(siteId=self.__siteId, verbose=self.__verbose)
            rL = cr.getContentTypes()
            logger.info("Content type definitions %r", rL)
        except:  # noqa: E722 pylint: disable=bare-except
            logger.exception("Failing test")
            self.fail()

        endTime = time.time()
        logger.info("Completed ad (%.2f seconds)", endTime - startTime)

    def testSummaryReport(self):
        """Test case -  create summary report"""
        startTime = time.time()
        logger.info("Starting")

        try:
            cr = ContentRequestReportDb(siteId=self.__siteId, verbose=self.__verbose)
            ctL = cr.getContentTypes()
            for ct in ctL:
                if ct.startswith("report-summary-"):
                    cD = cr.getContentTypeDef(ct)
                    logger.info("Content definition %r", cD)
                    rD = cr.extractContent(ct)
                    logger.info("Database content length %r", len(rD))
                    ss = json.dumps(rD)
                    logger.info("JSON serialized result length %r", len(ss))
        except:  # noqa: E722 pylint: disable=bare-except
            logger.exception("Failing test")
            self.fail()

        endTime = time.time()
        logger.info("Completed ad (%.2f seconds)\n" % endTime - startTime)


def suiteSummaryReport():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ContentRequestReportDbTests("testContentTypeReader"))
    suiteSelect.addTest(ContentRequestReportDbTests("testSummaryReport"))
    return suiteSelect


if __name__ == "__main__":
    #
    mySuite = suiteSummaryReport()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
