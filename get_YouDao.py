# _*_ coding:utf-8 _*_
# Created 2017/7/4
# @author:xu qi dong
# 获取有道晨读列表
# 每隔一天抓取有道精选列表数据存到数据库中

from myblog.wsgi import *
from threading import Timer
import json
import urllib2
from mylog import MyLog as mylog
from blog.models import YouDao
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class GetYouDaoList(object):
    #  这个类用于获取有道晨读列表
    def __init__(self):
        self.log = mylog()
        allTime = self.getAllDateTime()
        print allTime
        for time in allTime:
            self.getUrls(time)

        t = Timer(24*60*60, GetYouDaoList)  # 24*60*60 没个一天执行一次
        t.start()

    def getAllDateTime(self):
        allTime = []
        now = datetime.datetime.now()
        # for i in range(1, 30):
        #     delta = datetime.timedelta(days=-i)
        #     n_days = now + delta
        #     allTime.append(n_days.strftime('%Y-%m-%d'))
        allTime.append(now.strftime('%Y-%m-%d'))
        return allTime


    def getUrls(self, time):
        # 获取数据来源网页
        # start 2013 - 06 - 24
        URL= r'https://dict.youdao.com/infoline?apiversion=2&mode=publish&client=deskdict&keyfrom=dict2.index&startDate=' + time + '&callback=vistaCallback'
        htmlContent = self.getResponseContent(URL)
        htmlContent = htmlContent.lstrip('vistaCallback')
        htmlContent = htmlContent[1:len(htmlContent) - 1]
        # print htmlContent
        jsonData = json.loads(htmlContent, 'UTF-8')
        jsonList = jsonData[time]
        print jsonList
        # for one in jsonList:
        #     if one.has_key('type') and one.has_key('channelName'):
        #         YouDao.objects.get_or_create(
        #             title='{}'.format(unicode(one['title'])),
        #             type='{}'.format(one['type']),
        #             channelName='{}'.format(one['channelName']),
        #             url='{}'.format(one['url']),
        #             image_desk='{}'.format(one['image-desk']),
        #             audiourl='{}'.format(one['audiourl']),
        #             videourl='{}'.format(one['videourl']),
        #             time='{}'.format(one['time'])[0:8],
        #             slug='{}'.format(one['id']),
        #         )[0]
        #         print one['type'] + one['title']

    # 获取url内的json内容
    def getResponseContent(self, url):
        request = urllib2.Request(url)
        try:
            response = urllib2.urlopen(request)
        except:
            self.log.error(u'Python 返回URL:%s 数据失败' %url)
        else:
            self.log.info(u'Python 返回URL:%s 数据成功' % url)
            return response.read()


if __name__ == '__main__':
    GET = GetYouDaoList()
