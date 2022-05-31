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

import platform

import json
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
