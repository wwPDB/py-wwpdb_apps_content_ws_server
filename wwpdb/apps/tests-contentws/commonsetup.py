import sys
import os
import platform

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TESTOUTPUT = os.path.join(HERE, "test-output", platform.python_version())
if not os.path.exists(TESTOUTPUT):
    os.makedirs(TESTOUTPUT)

# We do this here - as unittest loads all at once - need to insure common

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock  # noqa: F401

configInfo = {
    "SITE_SERVICE_REGISTRATION_DIR_PATH": TESTOUTPUT,
    "SITE_SERVICE_REGISTRATION_KEY": "SOMEKEY",
}


class ConfigInfoReplace(object):
    def __init__(self, siteId=None, verbose=True, log=None):
        pass

    def get(self, keyWord, default=None):
        if keyWord in configInfo:
            return configInfo[keyWord]
        else:
            return default


def getSiteIdReplace(defaultSiteId=None):  # pylint: disable=unused-argument
    return "WWPDB_DEPLOY"


sys.modules["wwpdb.utils.config.ConfigInfo"] = Mock(ConfigInfo=ConfigInfoReplace, getSiteId=getSiteIdReplace)
