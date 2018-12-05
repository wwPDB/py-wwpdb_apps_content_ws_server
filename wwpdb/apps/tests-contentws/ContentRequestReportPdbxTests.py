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


import unittest
import time
import logging
import json
import os
import platform

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TESTOUTPUT = os.path.join(HERE, 'test-output', platform.python_version())
if not os.path.exists(TESTOUTPUT):
    os.makedirs(TESTOUTPUT)
mockTopPath = os.path.join(TOPDIR, 'wwpdb', 'mock-data')
rwMockTopPath = os.path.join(TESTOUTPUT)

# Must create config file before importing ConfigInfo
from wwpdb.utils.testing.SiteConfigSetup import SiteConfigSetup
from wwpdb.utils.testing.CreateRWTree import CreateRWTree
# Copy site-config and selected items
crw = CreateRWTree(mockTopPath, TESTOUTPUT)
crw.createtree(['site-config', 'wsresources'])
# Use populate r/w site-config using top mock site-config
SiteConfigSetup().setupEnvironment(rwMockTopPath, rwMockTopPath)

from wwpdb.apps.content_ws_server.content.ContentRequestReportPdbx import ContentRequestReportPdbx

FORMAT = '[%(levelname)s]-%(module)s.%(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class ContentRequestReportPdbxTests(unittest.TestCase):

    def setUp(self):
        self.__verbose = True
        self.__pdbxFilePath = os.path.join(mockTopPath, 'MODELS', "1kip.cif")
        self.__logFilePath = "my.log"


    def tearDown(self):
        pass

    def testEntryReader(self):
        """Test case -  report type status
        """
        startTime = time.clock()
        logger.info("Starting")

        try:
            cr = ContentRequestReportPdbx(self.__verbose)
            rD = cr.readFilePdbx(self.__pdbxFilePath, self.__logFilePath, ['entity', 'entity_poly', 'database_2'])
            logger.info("Data file content %r" % rD)
        except:
            logger.exception("Failing test")
            self.fail()

        endTime = time.clock()
        logger.info("Completed ad (%.2f seconds)\n" % (endTime - startTime))

    def testContentTypeReader(self):
        """Test case -  report type status
        """
        startTime = time.clock()
        logger.info("Starting")

        try:
            cr = ContentRequestReportPdbx(self.__verbose)
            rL = cr.getContentTypes()
            logger.info("Content type definitions %r" % rL)
        except:
            logger.exception("Failing test")
            self.fail()

        endTime = time.clock()
        logger.info("Completed ad (%.2f seconds)\n" % (endTime - startTime))

    def testEntryReport(self):
        """Test case -  report type status
        """
        startTime = time.clock()
        logger.info("Starting")

        try:
            cr = ContentRequestReportPdbx(self.__verbose)
            ctypeL = cr.getContentTypes()
            self.assertNotEqual(ctypeL, [], 'Could not parse content types')
            for ctype in ctypeL:
                if ctype.startswith("report-entry-"):
                    logger.info("Definition %r" % ctype)
                    rD = cr.extractContent(self.__pdbxFilePath, self.__logFilePath, ctype)
                    logger.info("File content %r" % rD)
                    # 1kip has three entity_poly
                    self.assertEqual(len(rD['entity_poly']), 3)
                    ss = json.dumps(rD)
                    logger.info("JSON serialized result %r" % ss)
        except:
            logger.exception("Failing test")
            self.fail()

        endTime = time.clock()
        logger.info("Completed ad (%.2f seconds)\n" % (endTime - startTime))


def suiteEntryReport():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ContentRequestReportPdbxTests("testEntryReader"))
    suiteSelect.addTest(ContentRequestReportPdbxTests("testContentTypeReader"))
    suiteSelect.addTest(ContentRequestReportPdbxTests("testEntryReport"))
    return suiteSelect


if __name__ == '__main__':
    #
    if (True):
        mySuite = suiteEntryReport()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
