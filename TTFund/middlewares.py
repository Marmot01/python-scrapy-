# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from TTFund.settings import USER_AGENT_LIST
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

#随机请求头

class RandomUserAgent(object):


    def process_request(self,request,spider):

        user = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = user

        #不写return,则直接交给下载器
        #return则返回给调度器

