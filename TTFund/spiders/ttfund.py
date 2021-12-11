import scrapy
from TTFund.items import TtfundItem
import json
import execjs

class TtfundSpider(scrapy.Spider):
    name = 'ttfund'#爬虫的名字
    allowed_domains = ['eastmoney.com']
    #start_urls = ['http://fund.eastmoney.com/jzzzl.html']

    start_urls = ['http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?&page=1,100']#可以通过设置最后一个数选择爬取多少数据

    def parse(self, response):
        print(response.request.headers)

        data = response.body.decode('utf-8')
        #返回的数据格式为js格式
        jsContent = execjs.compile(data)
        data_dict = jsContent.eval('db')
        datas = data_dict['datas']
        for data in datas:
            temp = {}
            temp['fund_code'] = data[0]
            temp['fund_name'] = data[1]
            temp['fund_link'] = "http://fund.eastmoney.com/"+data[0]+".html"
            detail_link = temp['fund_link']
            #print(detail_link)

        # nodelists = response.xpath('//*[@id="oTable"]/tbody/tr')
        # for node in nodelists:
        #     temp = {}
        #     temp['fund_code'] = node.xpath('./td[4]/text()').extract_first()
        #     temp['fund_name'] = node.xpath('./td[5]/nobr/a[1]/text()').extract_first()
        #     temp['fund_link'] = response.urljoin(node.xpath('./td[5]/nobr/a[1]/@href').extract_first())
        #     detail_link = temp['fund_link']

            #模拟点击链接
            yield scrapy.Request(
                url=detail_link,
                meta={'temp':temp},
                callback=self.parse_detail,
            )

    def parse_detail(self,response):
        temp = response.meta['temp']

        temp['fund_current_value'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[1]/dl[2]/dd[1]/span[1]/text()').extract_first()
        hisetory_link = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[1]/dl[2]/dt/p/span/span/a/@href').extract_first()
        temp['fund_current_date'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[1]/dl[2]/dt/p/text()').extract_first().strip(')')
        temp['fund_total_value'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[1]/dl[3]/dd[1]/span/text()').extract_first()
        temp['one_month_rate'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[1]/dl[1]/dd[2]/span[2]/text()').extract_first()
        temp['three_month_rate'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[1]/dl[2]/dd[2]/span[2]/text()').extract_first()
        temp['six_month_rate'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[1]/dl[3]/dd[2]/span[2]/text()').extract_first()
        temp['one_year_rate'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[1]/dl[1]/dd[3]/span[2]/text()').extract_first()
        temp['three_year_rate'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[1]/dl[2]/dd[3]/span[2]/text()').extract_first()
        temp['total_rate'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[1]/dl[3]/dd[3]/span[2]/text()').extract_first()

        #要去掉xpath中给tbody
        temp['fund_start_time'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[2]/table/tr[2]/td[1]/text()').extract_first().strip(': ')
        temp['fund_manager'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[2]/table/tr[1]/td[3]/a/text()').extract_first()
        temp['fund_size'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[2]/table/tr[1]/td[2]/text()').extract_first().strip(': ')
        temp['fund_risk'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[2]/table/tr[1]/td[1]/text()[2]').extract_first().strip('\xa0\xa0|\xa0\xa0')
        temp['fund_type'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[2]/table/tr[1]/td[1]/a/text()').extract_first()
        temp['fund_rating'] = response.xpath('//*[@id="body"]/div[11]/div/div/div[3]/div[1]/div[2]/table/tr[2]/td[3]/div/text()').extract_first()

        #print(temp)
        headers = {
            'Referer': hisetory_link,
        }

        kw = {'fundCode': temp['fund_code'],
                'pageIndex': 1,
                'pageSize': 5000,}#可以设置想要爬取的数据数量，如果设置数据多余网站总的数据，则只会爬取网站的总数据

        yield scrapy.Request(
            url="http://api.fund.eastmoney.com/f10/lsjz?fundCode={}&pageIndex={}&pageSize={}".format(temp['fund_code'],1,5000),
            headers=headers,
            meta={'temp':temp},
            callback=self.parse_history
        )

    def parse_history(self,response):
        temp = response.meta['temp']
        history_value = []
        dict_data = json.loads(response.body.decode())
        for data in dict_data['Data']['LSJZList']:
            tp = {}
            tp['净值日期'] = data['FSRQ']
            tp['单位净值'] = data['DWJZ']
            tp['累计净值'] = data['LJJZ']
            history_value.append(tp)

        items = TtfundItem()

        items['fund_code'] = temp['fund_code']
        items['fund_name'] = temp['fund_name']
        items['fund_link'] = temp['fund_link']

        items['fund_current_value'] = temp['fund_current_value']
        items['fund_current_date'] = temp['fund_current_date']
        items['fund_total_value'] = temp['fund_total_value']
        items['one_month_rate'] = temp['one_month_rate']
        items['three_month_rate'] = temp['three_month_rate']
        items['six_month_rate'] = temp['six_month_rate']
        items['one_year_rate'] = temp['one_year_rate']
        items['three_year_rate'] = temp['three_year_rate']
        items['total_rate'] = temp['total_rate']

        items['fund_start_time'] = temp['fund_start_time']
        items['fund_manager'] = temp['fund_manager']
        items['fund_size'] = temp['fund_size']
        items['fund_risk'] = temp['fund_risk']
        items['fund_type'] = temp['fund_type']
        items['fund_rating'] = temp['fund_rating']

        items['history_value'] =history_value

        yield items
