# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TtfundItem(scrapy.Item):
    # define the fields for your item here like:
    #基金代码
    fund_code = scrapy.Field()
    #基金简称
    fund_name = scrapy.Field()
    #基金链接
    fund_link = scrapy.Field()

    #当前单位净值
    fund_current_value = scrapy.Field()
    #当前日期
    fund_current_date = scrapy.Field()
    #累计净值
    fund_total_value = scrapy.Field()
    #近一月涨跌
    one_month_rate = scrapy.Field()
    #近三月涨跌
    three_month_rate = scrapy.Field()
    #近六月涨跌
    six_month_rate = scrapy.Field()
    #近一年涨跌
    one_year_rate = scrapy.Field()
    #近三年涨跌
    three_year_rate = scrapy.Field()
    #成立以来涨跌
    total_rate = scrapy.Field()

    #成立时间
    fund_start_time = scrapy.Field()
    #基金经理
    fund_manager = scrapy.Field()
    #基金规模
    fund_size = scrapy.Field()
    #基金类型
    fund_type = scrapy.Field()
    # 基金风险
    fund_risk = scrapy.Field()
    #基金评级
    fund_rating = scrapy.Field()

    #历史净值
    history_value = scrapy.Field()

