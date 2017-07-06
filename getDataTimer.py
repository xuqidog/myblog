# 定时后台执行脚本demo
from threading import Timer
import datetime


def printHello():
    print "Hello World"
    # self.log.info(u'%s' % datetime.datetime.now())
    fileName = u'timer.txt'.encode('utf8')
    with open(fileName, 'w') as fp:
            fp.write('%s' % datetime.datetime.now())
    t = Timer(2, printHello)
    t.start()


if __name__ == "__main__":
    printHello()