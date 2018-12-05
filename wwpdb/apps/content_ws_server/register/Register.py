##
# File:     Register.py
# Created:  15-Feb-2017
# Updates:
##
"""
Off-line API registration -

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.07"

import sys
import logging
from wwpdb.utils.ws_utils.TokenUtils import JwtTokenUtils


# Create logger
logger = logging.getLogger()
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


class Register(object):
    """  Off-line API registration -
    """
    def __init__(self):
        pass
        #

    def makeAccessToken(self, emailAddress, tokenPrefix="CONTENTWS", expireDays=30, tokenFileName="onedep_biocuration_apikey.jwt"):
        '''Test acquire new or existing token and write to disk
        '''
        try:
            tU = JwtTokenUtils(tokenPrefix=tokenPrefix)
            tokenId, jwtToken = tU.getToken(emailAddress, expireDays=expireDays)
            logging.info("For e-mail %r tokenid %r is %r " % (emailAddress, tokenId, jwtToken))
            tD = tU.parseToken(jwtToken)
            logging.info("token %r payload %r " % (tokenId, tD))
            #
            with open(tokenFileName, 'wb') as outfile:
                outfile.write("%s" % jwtToken)
            logging.info("token written to %r " % tokenFileName)
            ok = True
        except:
            logging.exception("Making token failed")
            ok = False
        return ok


if __name__ == '__main__':
    if len(sys.argv) < 3:
        # Use test case if no arguments are provided -
        emailAddress = "jdwestbrook@gmail.com"
        tokenPrefix = "CONTENTWS"
        expireDays = 30
    else:
        emailAddress = sys.argv[1]
        tokenPrefix = sys.argv[2]
        expireDays = int(str(sys.argv[3]))
    ##
    ##
    reg = Register()
    reg.makeAccessToken(emailAddress, tokenPrefix=tokenPrefix, expireDays=expireDays)
