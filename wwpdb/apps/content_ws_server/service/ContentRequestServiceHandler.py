#
# File:  ContentRequestServiceHandler (adapted from DetachedMessageConsumerExample.py)
# Date:  13-Feb-2017
#
#  Contolling wrapper for content request service consumer client -
#
#  Updates:
#  18-Feb-2017  jdw switch to using default ampq connection url
#
##

import json
import logging
import os
import platform
import sys
import time

try:
    from argparse import ArgumentParser as ArgParser
except ImportError:
    from optparse import OptionParser as ArgParser

# from optparse import OptionParser

from wwpdb.utils.detach.DetachedProcessBase import DetachedProcessBase
from wwpdb.utils.message_queue.MessageConsumerBase import MessageConsumerBase
from wwpdb.utils.message_queue.MessageQueueConnection import MessageQueueConnection
from wwpdb.utils.config.ConfigInfo import ConfigInfo, getSiteId

from wwpdb.apps.content_ws_server.content.ContentRequest import ContentRequest

logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG,
    format="\n%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s",
)


class MessageConsumer(MessageConsumerBase):
    def __init__(self, amqpUrl):
        super(MessageConsumer, self).__init__(amqpUrl)

    def workerMethod(self, msgBody, deliveryTag=None):
        try:
            # logger.debug("Message body %r" % msgBody)
            pD = json.loads(msgBody)
        except:
            logger.error("Message format error - discarding")
            return False
        #
        successFlag = True
        try:
            # logger.info("Message body %r" % pD)
            v = ContentRequest()
            v.setup(pD)
            v.run()
        except:
            logger.exception("Failed service execution with message %r" % pD)

        return successFlag


class MessageConsumerWorker(object):
    def __init__(self):
        self.__setup()

    def __setup(self):
        mqc = MessageQueueConnection()
        url = mqc._getDefaultConnectionUrl()
        self.__mc = MessageConsumer(amqpUrl=url)
        self.__mc.setQueue(queueName="contentws_queue", routingKey="contentws_requests")
        self.__mc.setExchange(exchange="biocurationws_exchange", exchangeType="topic")
        #

    def run(self):
        """  Run async consumer
        """
        startTime = time.time()
        logger.info("Starting ")
        try:
            try:
                logger.info("Run consumer worker starts")
                self.__mc.run()
            except KeyboardInterrupt:
                self.__mc.stop()
        except:
            logger.exception("MessageConsumer failing")

        endTime = time.time()
        logger.info("Completed (%.3f seconds)" % (endTime - startTime))

    def suspend(self):
        logger.info("Suspending consumer worker... ")
        self.__mc.stop()


class MyDetachedProcess(DetachedProcessBase):
    """  This class implements the run() method of the DetachedProcessBase() utility class.

         Illustrates the use of python logging and various I/O channels in detached process.
    """

    def __init__(
        self,
        pidFile="/tmp/DetachedProcessBase.pid",
        stdin=os.devnull,
        stdout=os.devnull,
        stderr=os.devnull,
        wrkDir="/",
        gid=None,
        uid=None,
    ):
        super(MyDetachedProcess, self).__init__(
            pidFile=pidFile,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            wrkDir=wrkDir,
            gid=gid,
            uid=uid,
        )
        self.__mcw = MessageConsumerWorker()

    def run(self):
        logger.info("STARTING detached run method")
        self.__mcw.run()

    def suspend(self):
        logger.info("SUSPENDING detached process")
        try:
            self.__mcw.suspend()
        except:
            pass


def main():
    # adding a conservative permission mask for this
    # os.umask(0o022)
    #
    siteId = getSiteId(defaultSiteId=None)
    cI = ConfigInfo(siteId)

    #    topPath = cI.get('SITE_WEB_APPS_TOP_PATH')
    topSessionPath = cI.get("SITE_WEB_APPS_TOP_SESSIONS_PATH")

    #
    myFullHostName = platform.uname()[1]
    myHostName = str(myFullHostName.split(".")[0]).lower()
    #
    wsLogDirPath = os.path.join(topSessionPath, "ws-logs")
    if not os.path.exists(wsLogDirPath):
        os.makedirs(wsLogDirPath)

    #  Setup logging  --
    now = time.strftime("%Y-%m-%d", time.localtime())

    description = "Content request service handler"
    parser = ArgParser(description=description)
    # py 2/3 issue  for optparse.OptionParser add an `add_argument` method for
    # compatibility with argparse.ArgumentParser
    try:
        parser.add_argument = parser.add_option
    except AttributeError:
        pass

    parser.add_argument(
        "--start",
        default=False,
        action="store_true",
        dest="startOp",
        help="Start consumer client process",
    )
    parser.add_argument(
        "--stop",
        default=False,
        action="store_true",
        dest="stopOp",
        help="Stop consumer client process",
    )
    parser.add_argument(
        "--restart",
        default=False,
        action="store_true",
        dest="restartOp",
        help="Restart consumer client process",
    )
    parser.add_argument(
        "--status",
        default=False,
        action="store_true",
        dest="statusOp",
        help="Report consumer client process status",
    )

    # parser.add_argument("-v", "--verbose", default=False, action="store_true", dest="verbose", help="Enable verbose output")
    parser.add_argument(
        "--debug",
        default=1,
        type=int,
        dest="debugLevel",
        help="Debug level (default: 1 [0-3]",
    )
    parser.add_argument(
        "--instance",
        default=1,
        type=int,
        dest="instanceNo",
        help="Instance number [1-n]",
    )
    #
    # (options, args) = parser.parse_args()

    options = parser.parse_args()
    if isinstance(options, tuple):
        args = options[0]
    else:
        args = options
    del options

    #
    pidFilePath = os.path.join(
        wsLogDirPath, myHostName + "_" + str(args.instanceNo) + ".pid"
    )
    stdoutFilePath = os.path.join(
        wsLogDirPath, myHostName + "_" + str(args.instanceNo) + "_stdout.log"
    )
    stderrFilePath = os.path.join(
        wsLogDirPath, myHostName + "_" + str(args.instanceNo) + "_stderr.log"
    )
    wfLogFilePath = os.path.join(
        wsLogDirPath, myHostName + "_" + str(args.instanceNo) + "_" + now + ".log"
    )
    #
    logger = logging.getLogger(name="root")
    logging.captureWarnings(True)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s"
    )
    handler = logging.FileHandler(wfLogFilePath)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    #
    lt = time.strftime("%Y %m %d %H:%M:%S", time.localtime())
    #
    if args.debugLevel > 2:
        logger.setLevel(logging.DEBUG)
        logger.debug("Setting DEBUG logging")
    elif args.debugLevel > 0:
        logger.setLevel(logging.INFO)
        logger.debug("Setting INFO logging")
    else:
        logger.setLevel(logging.ERROR)
    #
    #
    myDP = MyDetachedProcess(
        pidFile=pidFilePath,
        stdout=stdoutFilePath,
        stderr=stderrFilePath,
        wrkDir=wsLogDirPath,
    )

    if args.startOp:
        sys.stdout.write(
            "+DetachedMessageConsumer() starting consumer service at %s\n" % lt
        )
        logger.info("DetachedMessageConsumer() starting consumer service at %s" % lt)
        myDP.start()
    elif args.stopOp:
        sys.stdout.write(
            "+DetachedMessageConsumer() stopping consumer service at %s\n" % lt
        )
        logger.info("DetachedMessageConsumer() stopping consumer service at %s" % lt)
        myDP.stop()
    elif args.restartOp:
        sys.stdout.write(
            "+DetachedMessageConsumer() restarting consumer service at %s\n" % lt
        )
        logger.info("DetachedMessageConsumer() restarting consumer service at %s" % lt)
        myDP.restart()
    elif args.statusOp:
        sys.stdout.write(
            "+DetachedMessageConsumer() reporting status for consumer service at %s\n"
            % lt
        )
        sys.stdout.write(myDP.status())
    else:
        pass


if __name__ == "__main__":
    main()
